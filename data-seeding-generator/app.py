from flask import Flask, render_template, request, jsonify, send_file
import logging
import time
import random
import io
import pandas as pd
from services.db_writer import get_ids_from_db, get_connection
from generators.manager import DataGenerationManager

# ==========================================
# CONFIGURACIÓN INICIAL
# ==========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Mapeo completo de tablas para evitar errores de referencia
TABLAS_MAP = {
    'roles': 'Roles',
    'usuarios': 'Usuarios',
    'proveedores': 'Proveedores',
    'clientes': 'Clientes',
    'motos': 'Motos',
    'reparaciones': 'Reparaciones',
    'facturas': 'Facturas',
    'pagos': 'Pagos',
    'inventario': 'Inventario',
    'servicios': 'Servicios',
    'citas': 'Citas'
}

# ==========================================
# UTILIDADES DE DATOS
# ==========================================
def obtener_conteo_seguro(query):
    """
    Maneja el retorno de get_ids_from_db para asegurar que siempre
    obtengamos un valor numérico, evitando el error 'int object is not subscriptable'.
    """
    try:
        res = get_ids_from_db(query)
        # Si es una lista de listas: [[valor]]
        if isinstance(res, list) and len(res) > 0:
            if isinstance(res[0], (list, tuple)):
                return res[0][0] if res[0][0] is not None else 0
            return res[0] if res[0] is not None else 0
        # Si ya es un entero o flotante directo
        if isinstance(res, (int, float)):
            return res
        return 0
    except Exception as e:
        logger.warning(f"Error en consulta de conteo: {e}")
        return 0

# ==========================================
# RUTA PRINCIPAL (DASHBOARD)
# ==========================================
@app.route('/')
def index():
    try:
        # Consultas con validación de tipo de dato
        stats = {
            'clientes': obtener_conteo_seguro("SELECT COUNT(*) FROM Clientes"),
            'motos': obtener_conteo_seguro("SELECT COUNT(*) FROM Motos"),
            'servicios': obtener_conteo_seguro("SELECT COUNT(*) FROM Reparaciones"),
            'ingresos': obtener_conteo_seguro("SELECT SUM(Monto) FROM Pagos"),
            'stock': obtener_conteo_seguro("SELECT SUM(Cantidad) FROM Inventario")
        }
        
        # Formateo de moneda para la UI
        stats['ingresos'] = f"{float(stats['ingresos']):,.2f}"
        db_status = "ACTIVE"
    except Exception as e:
        logger.error(f"⚠️ ERROR DASHBOARD: {e}")
        stats = {'clientes': 0, 'motos': 0, 'servicios': 0, 'ingresos': "0.00", 'stock': 0}
        db_status = "ERROR"

    return render_template('index.html', stats=stats, db_status=db_status)

# ==========================================
# MOTOR DE INYECCIÓN MODULAR
# ==========================================
@app.route('/ejecutar', methods=['POST'])
def ejecutar():
    try:
        config = request.json
        if not config:
            return jsonify({"status": "error", "message": "No se recibió configuración"}), 400

        tabla_key = config.get('tabla')
        n_registros = int(config.get('n', 10))
        seed = config.get('seed')
        
        # Reproducibilidad
        if seed and str(seed).strip():
            random.seed(int(seed))

        start_time = time.time()
        
        # Configuración para el Manager
        manager_config = {tabla_key: n_registros}
        manager = DataGenerationManager(manager_config)
        
        # Ejecución del motor
        manager.run()
        
        duracion = time.time() - start_time
        
        return jsonify({
            "status": "success", 
            "message": f"Inyección en {tabla_key.upper()} completada con éxito",
            "metrics": {
                "tiempo": f"{duracion:.2f}s",
                "registros": n_registros
            }
        })
    except Exception as e:
        logger.critical(f"❌ ERROR EN EJECUCIÓN: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ==========================================
# SISTEMA DE EXPORTACIÓN ROBUSTO
# ==========================================
@app.route('/exportar/<formato>/<entidad>')
def exportar(formato, entidad):
    try:
        tabla_real = TABLAS_MAP.get(entidad.lower(), entidad.capitalize())
        
        conn = get_connection()
        query = f"SELECT * FROM {tabla_real}"
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            return f"La tabla {tabla_real} está vacía.", 400

        # --- EXPORTAR A CSV ---
        if formato == 'csv':
            output = io.StringIO()
            df.to_csv(output, index=False, encoding='utf-8-sig')
            mem = io.BytesIO(output.getvalue().encode('utf-8-sig'))
            return send_file(
                mem,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f"CasaTuning_{tabla_real}.csv"
            )

        # --- EXPORTAR A EXCEL ---
        elif formato == 'excel':
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name=tabla_real)
                # Auto-ajuste de columnas en Excel
                worksheet = writer.sheets[tabla_real]
                for idx, col in enumerate(df.columns):
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(idx, idx, max_len)
            
            output.seek(0)
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=f"Reporte_{tabla_real}.xlsx"
            )

        # --- EXPORTAR A SCRIPT SQL ---
        elif formato == 'sql':
            lines = [f"-- Dump Casa Tuning Engine\nUSE [TallerMotosTunig];\nGO\n"]
            for _, row in df.iterrows():
                cols = ", ".join([f"[{c}]" for c in row.index])
                vals = []
                for v in row.values:
                    if pd.isna(v): vals.append("NULL")
                    elif isinstance(v, str): vals.append(f"'{v.replace("'", "''")}'")
                    elif isinstance(v, (int, float)): vals.append(str(v))
                    else: vals.append(f"'{str(v)}'")
                
                lines.append(f"INSERT INTO {tabla_real} ({cols}) VALUES ({', '.join(vals)});")
            
            mem = io.BytesIO("\n".join(lines).encode('utf-8'))
            return send_file(
                mem,
                mimetype='text/plain',
                as_attachment=True,
                download_name=f"Backup_{tabla_real}.sql"
            )

    except Exception as e:
        logger.error(f"Error exportando: {e}")
        return jsonify({"status": "error", "message": f"Error al exportar: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)