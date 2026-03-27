import pyodbc
import logging

# ==============================
# CONFIGURACIÓN
# ==============================
SERVER = "DESKTOP-U11P2A7"
DATABASE = "TallerMotosTunig"

# Cadena de conexión optimizada para SQL Server con Windows Authentication
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={"DESKTOP-U11P2A7"};"
    f"DATABASE={"TallerMotosTunig"};"
    "Trusted_Connection=yes;"
    "Timeout=30;"
)

# Configuración de logs para ver qué pasa en la consola
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================
# 🔌 CONEXIÓN
# ==============================
def get_connection():
    """Establece la conexión con la base de datos."""
    try:
        return pyodbc.connect(CONN_STR)
    except Exception as e:
        logger.error(f"❌ Error conectando a SQL Server: {e}")
        raise Exception(f"No se pudo conectar a la DB: {e}")

# ==============================
# 📥 INSERCIÓN MASIVA (Versión Final Compatible)
# ==============================
def insert_massive(query, data_source):
    """
    Inserta datos usando fast_executemany.
    Soporta tanto listas como generadores.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True

    try:
        # Convertimos a lista solo si es necesario para el executemany
        # Si es un generador, lo convertimos a lista aquí
        data_list = list(data_source) if not isinstance(data_source, list) else data_source
        
        if not data_list:
            logger.warning("⚠️ No hay datos para insertar.")
            return

        cursor.executemany(query, data_list)
        conn.commit()
        logger.info(f"✅ {len(data_list)} registros insertados correctamente.")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Error en inserción masiva: {e}")
        raise e
    finally:
        conn.close()

# ==============================
# 📊 CONSULTA DE DATOS E IDS
# ==============================
def get_ids_from_db(query, params=None):
    """
    Recupera datos de la DB. 
    - Si la consulta pide 1 columna, devuelve una lista simple [1, 2, 3]
    - Si pide varias, devuelve una lista de tuplas [(1, 'A'), (2, 'B')]
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params or [])
        rows = cursor.fetchall()
        
        if not rows:
            return []

        # Lógica inteligente: 
        # Si la fila tiene solo un elemento, devolvemos el valor directo.
        # Si tiene más (ej: IdReparacion, IdMoto), devolvemos la fila completa.
        if len(rows[0]) == 1:
            return [row[0] for row in rows]
        else:
            return [list(row) for row in rows]

    except Exception as e:
        logger.warning(f"⚠️ Error ejecutando consulta: {e}")
        return []
    finally:
        conn.close()