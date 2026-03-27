import random
from decimal import Decimal

def generate_inventario(n, proveedor_ids):
    """
    Generador de inventario (piezas).
    n: Cantidad de registros a generar.
    proveedor_ids: Lista de IDs de proveedores existentes.
    """
    if not proveedor_ids:
        return

    # Base de datos de conocimiento de piezas (Expandible)
    prefijos = ['Kit de', 'Bomba de', 'Cable de', 'Juego de', 'Filtro de', 'Pastillas de']
    componentes = ['Aceite', 'Frenos', 'Embrague', 'Acelerador', 'Aire', 'Gasolina', 'Cadena']
    marcas = ['NGK', 'Motul', 'Castrol', 'Brembo', 'Michelin', 'Pirelli']

    # Piezas base para asegurar coherencia mínima
    piezas_base = [
        ('Aceite 10W40', 15.50), ('Filtro de Aceite', 8.25),
        ('Pastillas de Freno', 22.00), ('Bujía NGK', 5.75),
        ('Kit de Arrastre', 45.00), ('Batería 12V', 40.00)
    ]

    for i in range(n):
        if i < len(piezas_base):
            nombre, precio_base = piezas_base[i]
        else:
            # Generación sintética para grandes volúmenes
            nombre = f"{random.choice(prefijos)} {random.choice(componentes)} {random.choice(marcas)}"
            precio_base = random.uniform(5.00, 150.00)

        cantidad = random.randint(0, 100)
        # Usamos Decimal para evitar errores de redondeo en el millón de registros
        precio = (Decimal(str(precio_base)) + Decimal(str(random.uniform(0, 5)))).quantize(Decimal('0.01'))
        id_prov = random.choice(proveedor_ids)
        
        # ENTREGAMOS LA TUPLA
        # Orden: (NombrePieza, Cantidad, Precio_Actual, IdProveedor)
        yield (nombre, cantidad, precio, id_prov)