import random
from decimal import Decimal

def generate_detalle_reparacion(n, reparacion_ids, piezas_data):
    """
    Generador para los detalles de reparación (piezas utilizadas).
    n: Cantidad de registros de detalles a generar.
    reparacion_ids: IDs de la tabla 'Reparaciones'.
    piezas_data: Lista de tuplas [(IdPieza, Precio_Actual), ...]
    """
    if not reparacion_ids or not piezas_data:
        return

    for _ in range(n):
        id_reparacion = random.choice(reparacion_ids)
        
        # Seleccionamos qué pieza se usó en la reparación
        pieza = random.choice(piezas_data)
        id_pieza = pieza[0]
        
        # El precio de venta al cliente suele ser el precio actual de inventario
        precio_venta = Decimal(str(pieza[1])).quantize(Decimal('0.01'))
        
        # Cantidad de piezas usadas (ej. 1 kit de frenos, 2 litros de aceite)
        cantidad = random.randint(1, 4)
        
        # Subtotal del detalle
        subtotal = (precio_venta * cantidad).quantize(Decimal('0.01'))
        
        # ENTREGAMOS LA TUPLA
        # Orden sugerido: (IdReparacion, IdPieza, Cantidad, PrecioUnitario, Subtotal)
        yield (id_reparacion, id_pieza, cantidad, precio_venta, subtotal)