import random
from datetime import datetime, timedelta
from decimal import Decimal

def generate_pagos(facturas_pendientes):
    """
    Generador puro de pagos.
    facturas_pendientes: Lista de tuplas (IdFactura, MontoTotal) 
    que el orquestador obtuvo previamente.
    """
    if not facturas_pendientes:
        return

    metodos = ['Efectivo', 'Tarjeta', 'Transferencia', 'Pago Móvil']

    for id_fac, total in facturas_pendientes:
        # La fecha de pago suele ser el mismo día de la factura o un poco después
        fecha_pago = datetime.now() - timedelta(minutes=random.randint(5, 120))
        
        metodo = random.choice(metodos)
        
        # Aseguramos precisión con Decimal
        monto = Decimal(str(total)).quantize(Decimal('0.01'))
        
        # ENTREGAMOS LA TUPLA
        # Orden: (IdFactura, MetodoPago, Monto, FechaPago)
        yield (id_fac, metodo, monto, fecha_pago)