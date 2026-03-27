import random
from datetime import datetime, timedelta
from decimal import Decimal

def generate_compras_completas(n, prov_ids, piezas_data):
    """
    Generador dual para Compras y sus Detalles.
    n: Cantidad de Compras (cabeceras) a generar.
    prov_ids: Lista de IDs de proveedores.
    piezas_data: Lista de tuplas [(IdPieza, Precio_Actual), ...]
    """
    if not prov_ids or not piezas_data:
        return

    # Usaremos una lista temporal para guardar los IDs de compras generados en esta sesión
    # si es que tu DB no los genera automáticamente, o simplemente para el flujo.
    
    for i in range(n):
        id_compra = i + 1 # Asumiendo un ID secuencial para el ejercicio
        id_prov = random.choice(prov_ids)
        fecha = datetime.now() - timedelta(days=random.randint(0, 365))
        
        # --- LÓGICA DE DETALLES ---
        detalles_de_esta_compra = []
        total_compra = Decimal('0.00')
        
        # Generamos entre 2 y 5 piezas por cada compra
        num_items = random.randint(2, 5)
        for _ in range(num_items):
            pieza = random.choice(piezas_data)
            id_pieza = pieza[0]
            precio_u = (Decimal(str(pieza[1])) * Decimal('0.80')).quantize(Decimal('0.01'))
            cant = random.randint(5, 50)
            importe = (precio_u * cant).quantize(Decimal('0.01'))
            
            total_compra += importe
            
            # Guardamos el detalle para enviarlo después o procesarlo
            detalle = {
                'id_pieza': id_pieza,
                'cantidad': cant,
                'precio_u': precio_u,
                'importe': importe
            }
            detalles_de_esta_compra.append(detalle)

        # 1. YIELD de la CABECERA (Ya con el total calculado, evitamos el UPDATE posterior)
        # Orden: (IdCompra, IdProveedor, FechaCompra, MontoTotal)
        yield "CABECERA", (id_compra, id_prov, fecha, total_compra), detalles_de_esta_compra