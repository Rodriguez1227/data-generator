import random

def generate_reparacion_piezas(n, reparacion_ids, piezas_ids):
    """
    Generador para el detalle de piezas usadas en reparaciones.
    n: Cantidad total de registros de consumo a generar.
    reparacion_ids: Lista de IDs de la tabla Reparaciones.
    piezas_ids: Lista de IDs de la tabla Inventario.
    """
    if not reparacion_ids or not piezas_ids:
        return

    for _ in range(n):
        # Seleccionamos una reparación y una pieza al azar
        id_rep = random.choice(reparacion_ids)
        id_pieza = random.choice(piezas_ids)
        
        # Cantidad de piezas usadas en ese trabajo específico
        cantidad = random.randint(1, 4)
        
        # ENTREGAMOS LA TUPLA
        # Orden: (IdReparacion, IdPieza, CantidadUsada)
        yield (id_rep, id_pieza, cantidad)