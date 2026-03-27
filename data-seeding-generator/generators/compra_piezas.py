import random
from decimal import Decimal

def generate_compra_piezas(n, compra_ids, piezas_data):
    """
    Generador de los detalles de cada compra.
    n: Cantidad total de registros de detalles a generar.
    compra_ids: Lista de IDs de la tabla 'Compras' (Cabecera).
    piezas_data: Lista de tuplas [(IdPieza, Precio_Actual), ...] del inventario.
    """
    if not compra_ids or not piezas_data:
        return

    for _ in range(n):
        id_compra = random.choice(compra_ids)
        
        # Seleccionamos una pieza al azar del inventario disponible
        pieza = random.choice(piezas_data)
        id_pieza = pieza[0]
        precio_actual = Decimal(str(pieza[1])) # Convertimos a Decimal para precisión
        
        # Lógica de negocio: El precio de compra suele ser un 20% menor al de venta
        precio_unitario = (precio_actual * Decimal('0.80')).quantize(Decimal('0.01'))
        
        cantidad = random.randint(5, 50)
        importe = (cantidad * precio_unitario).quantize(Decimal('0.01'))
        
        # IdCompraPieza: Si tu DB no es Auto-Incremental, generamos uno aleatorio
        # Pero lo ideal es que sea IDENTITY/AUTO_INCREMENT en la DB.
        id_item = random.randint(100000, 999999) 
        
        # ENTREGAMOS LA TUPLA
        # El orden debe ser: (IdCompraPieza, IdPieza, IdCompra, CantidadComprada, PrecioUnitario, Importe)
        yield (id_item, id_pieza, id_compra, cantidad, precio_unitario, importe)