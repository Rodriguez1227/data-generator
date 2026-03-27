import time
import logging
import random
from services.db_writer import insert_massive, get_ids_from_db, get_connection

# Importación de generadores específicos
from .usuarios import generate_usuarios
from .clientes import generate_clientes
from .proveedores import generate_proveedores
from .servicios import generate_servicios
from .inventario import generate_inventario
from .motos import generate_motos
from .citas import generate_citas
from .reparaciones import generate_reparaciones_completas 

class DataGenerationManager:
    def __init__(self, config):
        """
        config: dict con la estructura {'tabla': n, 'batch': size, 'seed': value}
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

    def run(self):
        start_time = time.time()
        # Detectar la entidad a procesar (ej: 'usuarios', 'reparaciones', etc.)
        entidad = list(self.config.keys())[0]
        try:
            n = int(self.config[entidad])
        except (ValueError, KeyError):
            n = 10  # Valor por defecto

        print(f"🚀 MOTOR CASA TUNING: Iniciando flujo de {entidad.upper()} ({n} registros)")

        # --- PASO 0: CONFIGURACIÓN MAESTRA ---
        # Garantiza que existan Roles y Servicios base antes de inyectar
        self._check_base_config()

        # --- FLUJO 1: PERSONAL (USUARIOS) ---
        if entidad == 'usuarios':
            data = generate_usuarios(n)
            insert_massive(
                "INSERT INTO Usuarios (Nombre, Apellido, Telefono, Correo, Usuario, Contraseña, IdRol) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                data
            )

        # --- FLUJO 2: ABASTECIMIENTO (PROVEEDORES + INVENTARIO) ---
        elif entidad == 'proveedores':
            # 1. Insertar Proveedores
            insert_massive(
                "INSERT INTO Proveedores (Nombre, Telefono, Correo) VALUES (?, ?, ?)", 
                generate_proveedores(n)
            )
            
            # 2. Recuperar IDs de forma segura para asociar inventario
            raw_prov_ids = get_ids_from_db(f"SELECT TOP {n} IdProveedor FROM Proveedores ORDER BY IdProveedor DESC")
            prov_ids = [row[0] if isinstance(row, (list, tuple)) else row for row in raw_prov_ids]
            
            if prov_ids:
                print(f"📦 Abasteciendo Inventario para {len(prov_ids)} proveedores...")
                insert_massive(
                    "INSERT INTO Inventario (NombrePieza, Cantidad, Precio_Actual, IdProveedor) VALUES (?, ?, ?, ?)", 
                    generate_inventario(n * 2, prov_ids)
                )

        # --- FLUJO 3: CARTERA (CLIENTES + MOTOS + CITAS) ---
        elif entidad == 'clientes':
            # 1. Insertar Clientes
            insert_massive(
                "INSERT INTO Clientes (Nombre, Apellido, Telefono, Correo, Direccion, Usuario, Contraseña, IdRol) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                generate_clientes(n)
            )
            
            # 2. Recuperar IDs Clientes recién creados
            raw_cli_ids = get_ids_from_db(f"SELECT TOP {n} IdCliente FROM Clientes ORDER BY IdCliente DESC")
            cli_ids = [row[0] if isinstance(row, (list, tuple)) else row for row in raw_cli_ids]
            
            if cli_ids:
                print(f"🏍️ Registrando parque vehicular...")
                insert_massive(
                    "INSERT INTO Motos (IdCliente, Placa, Marca, Modelo, Año, Color) VALUES (?, ?, ?, ?, ?, ?)", 
                    generate_motos(n, cli_ids)
                )
                
                print(f"📅 Programando Citas...")
                insert_massive(
                    "INSERT INTO Citas (IdCliente, FechaCita, Estado, Hora, Descripcion) VALUES (?, ?, ?, ?, ?)", 
                    generate_citas(n, cli_ids)
                )

        # --- FLUJO 4: OPERACIONES (REPARACIONES + FACTURACION + PAGOS) ---
        elif entidad == 'reparaciones':
            # 1. Validar existencia de dependencias críticas
            raw_moto_ids = get_ids_from_db("SELECT IdMoto FROM Motos")
            moto_ids = [r[0] if isinstance(r, (list, tuple)) else r for r in raw_moto_ids]
            
            # Buscamos específicamente técnicos (IdRol = 2)
            raw_tec_ids = get_ids_from_db("SELECT IdUsuario FROM Usuarios WHERE IdRol = 2")
            tecnico_ids = [r[0] if isinstance(r, (list, tuple)) else r for r in raw_tec_ids]
            
            if not moto_ids or not tecnico_ids:
                raise Exception("❌ ERROR CRÍTICO: Se requieren Motos y Técnicos (IdRol=2) en la DB.")

            # 2. Extraer catálogos para costeo
            servicios_data = get_ids_from_db("SELECT IdServicio, Precio_Servicio FROM Servicios")
            piezas_data = get_ids_from_db("SELECT IdPieza, Precio_Actual FROM Inventario")

            if not servicios_data or not piezas_data:
                raise Exception("❌ ERROR: No hay 'Servicios' o 'Piezas' (Inventario) para generar reparaciones.")

            print(f"🔧 Iniciando {n} Reparaciones con {len(servicios_data)} servicios y {len(piezas_data)} piezas...")
            
            # 3. Generar datos (Asegurando 5 parámetros: IdMoto, IdUsuario, Descripcion, Estado, FechaInicio)
            reps_raw = generate_reparaciones_completas(n, moto_ids, tecnico_ids, servicios_data, piezas_data)
            
            # Si el generador devuelve un dict con 'reparaciones', lo extraemos; si no, usamos la lista
            data_to_insert = reps_raw['reparaciones'] if isinstance(reps_raw, dict) else reps_raw

            insert_massive(
                "INSERT INTO Reparaciones (IdMoto, IdUsuario, Descripcion, Estado, FechaInicio) VALUES (?, ?, ?, ?, ?)", 
                data_to_insert
            )

            # 4. Generar ciclo de cobro: Factura -> Pago
            print("💰 Procesando Facturación y Colecta...")
            last_reps_raw = get_ids_from_db(f"SELECT TOP {n} IdReparacion, IdMoto FROM Reparaciones ORDER BY IdReparacion DESC")
            
            facturas_data = []
            for row in last_reps_raw:
                id_rep, id_moto = row
                
                # Buscar el cliente dueño de la moto
                cli_res = get_ids_from_db(f"SELECT IdCliente FROM Motos WHERE IdMoto = {id_moto}")
                if cli_res:
                    id_cli = cli_res[0][0] if isinstance(cli_res[0], (list, tuple)) else cli_res[0]
                    
                    # Monto aleatorio basado en un rango de taller
                    monto = round(random.uniform(35.0, 250.0), 2)
                    facturas_data.append((id_cli, id_rep, monto, 'Pagada'))

            if facturas_data:
                insert_massive("INSERT INTO Facturas (IdCliente, IdReparacion, MontoTotal, Estado_Pago) VALUES (?, ?, ?, ?)", facturas_data)
                
                # Obtener IDs de facturas para registrar el flujo de caja (Pagos)
                raw_fac_ids = get_ids_from_db(f"SELECT TOP {len(facturas_data)} IdFactura, MontoTotal FROM Facturas ORDER BY IdFactura DESC")
                pagos_data = [(row[0], random.choice(['Efectivo', 'Transferencia', 'Tarjeta']), row[1]) for row in raw_fac_ids]
                
                insert_massive("INSERT INTO Pagos (IdFactura, MetodoPago, Monto) VALUES (?, ?, ?)", pagos_data)

        print(f"✅ ¡FLUJO FINALIZADO! Tiempo total: {round(time.time() - start_time, 2)}s")

    def _check_base_config(self):
        """Valida e inserta datos maestros necesarios para la integridad referencial."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Asegurar Roles Mínimos
        cursor.execute("SELECT COUNT(*) FROM Roles")
        if cursor.fetchone()[0] == 0:
            print("⚙️ Configurando Roles Base...")
            roles = [('Administrador',), ('Tecnico',), ('Cliente',)]
            cursor.executemany("INSERT INTO Roles (NombreRol) VALUES (?)", roles)
        
        # 2. Asegurar Catálogo de Servicios Mínimo
        cursor.execute("SELECT COUNT(*) FROM Servicios")
        if cursor.fetchone()[0] == 0:
            print("⚙️ Cargando Catálogo de Servicios inicial...")
            servs = [
                ('Mantenimiento Preventivo', 30.0),
                ('Cambio de Aceite Semi-Sintético', 20.0),
                ('Escaneo Computarizado', 45.0),
                ('Limpieza de Inyectores (Ultrasonido)', 50.0),
                ('Revisión de Sistema Eléctrico', 25.0)
            ]
            cursor.executemany("INSERT INTO Servicios (Servicio, Precio_Servicio) VALUES (?, ?)", servs)
            
        conn.commit()
        conn.close()