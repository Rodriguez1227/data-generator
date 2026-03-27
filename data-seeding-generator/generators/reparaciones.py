import random
from datetime import datetime, timedelta
from decimal import Decimal

def generate_reparaciones_completas(n, moto_ids, tecnico_ids, servicios_data, piezas_data):
    """
    Generador de datos para Reparaciones y sus detalles.
    Retorna un diccionario con listas de tuplas listas para insert_massive.
    """
    if not moto_ids or not tecnico_ids:
        return {'reparaciones': [], 'detalles': []}

    # Catálogos de estados y fallas para realismo
    descripciones_fallas = [
        "Mantenimiento preventivo de los 5,000km",
        "Ajuste de cadena y lubricación general",
        "Revisión de sistema eléctrico y luces",
        "Cambio de pastillas de freno y líquido",
        "Limpieza profunda de carburador/inyectores",
        "Reparación de fuga de aceite en cárter",
        "Instalación de accesorios tuning (Luces LED)",
        "Cambio de kit de arrastre completo"
    ]
    estados = ['Pendiente', 'En Proceso', 'Completado']

    reparaciones_list = []
    detalles_list = []

    for i in range(n):
        # --- 1. DATOS DE CABECERA (Reparaciones) ---
        id_moto = random.choice(moto_ids)
        id_tecnico = random.choice(tecnico_ids)
        fecha = datetime.now() - timedelta(days=random.randint(0, 60))
        descripcion = random.choice(descripciones_fallas)
        estado = random.choice(estados)

        # Guardamos la cabecera (5 campos según el INSERT del manager)
        # (IdMoto, IdUsuario, Descripcion, Estado, FechaInicio)
        reparaciones_list.append((
            id_moto, 
            id_tecnico, 
            descripcion, 
            estado, 
            fecha
        ))

        # --- 2. DATOS DE DETALLE (Detalle_Reparacion) ---
        # Seleccionamos un servicio y una pieza aleatoria para este trabajo
        serv = random.choice(servicios_data)
        pieza = random.choice(piezas_data)
        
        id_serv = serv[0]
        costo_serv = Decimal(str(serv[1]))
        
        id_pieza = pieza[0]
        costo_pieza = Decimal(str(pieza[1]))
        cant_pieza = random.randint(1, 3)
        
        # El importe del detalle se calcula para reportes futuros
        subtotal = costo_serv + (costo_pieza * cant_pieza)
        
        # Estructura para la tabla Detalle_Reparacion (ajustar según tu DB)
        # Nota: IdReparacion no se incluye aquí porque es IDENTITY, 
        # se suele asociar después o mediante procedimientos.
        detalles_list.append({
            'id_servicio': id_serv,
            'id_pieza': id_pieza,
            'cantidad': cant_pieza,
            'precio_unitario': costo_pieza,
            'subtotal': subtotal
        })

    return {
        'reparaciones': reparaciones_list,
        'detalles': detalles_list
    }