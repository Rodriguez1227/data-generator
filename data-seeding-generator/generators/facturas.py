import random
from datetime import datetime, timedelta
from decimal import Decimal

def generate_facturas(reparaciones_pendientes):
    """
    Generador puro de facturas.
    reparaciones_pendientes: Lista de tuplas o diccionarios con 
    (IdReparacion, IdCliente, Total) obtenidos previamente.
    """
    if not reparaciones_pendientes:
        return

    estados_pago = ['Pagado', 'Pendiente', 'Cancelado']

    for id_rep, id_cli, total in reparaciones_pendientes:
        # La fecha de factura suele ser igual o posterior a la reparación
        fecha_factura = datetime.now() - timedelta(days=random.randint(0, 5))
        
        # El 90% de las veces en un taller como Casa Tuning el pago es inmediato
        estado = random.choices(estados_pago, weights=[90, 8, 2])[0]
        
        # Aseguramos que el total sea Decimal para precisión financiera
        monto_total = Decimal(str(total)).quantize(Decimal('0.01'))
        
        # ENTREGAMOS LA TUPLA
        # Orden: (IdCliente, IdReparacion, FechaFactura, MontoTotal, Estado_Pago)
        yield (id_cli, id_rep, fecha_factura, monto_total, estado)