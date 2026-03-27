import random
from decimal import Decimal

def generate_servicios(n):
    """
    Generador de servicios para el taller.
    n: Cantidad total de servicios a generar.
    """
    # Tus servicios base reales
    servicios_base = [
        ('Cambio de aceite de motor', 25.00),
        ('Ajuste de frenos', 15.00),
        ('Lavado general', 15.00),
        ('Ajuste de cadena', 10.00),
        ('Diagnóstico computarizado', 20.00)
    ]

    # Extensiones para generar volumen si n > len(servicios_base)
    modificadores = ['Premium', 'Económico', 'Express', 'Completo', 'Especializado']
    sistemas = ['Eléctrico', 'de Transmisión', 'de Suspensión', 'de Motor', 'de Inyección']

    for i in range(n):
        if i < len(servicios_base):
            nombre, precio_base = servicios_base[i]
        else:
            # Generación sintética: "Ajuste de Motor Premium"
            nombre = f"{random.choice(['Mantenimiento', 'Ajuste', 'Revisión'])} {random.choice(sistemas)} {random.choice(modificadores)}"
            precio_base = random.uniform(10.00, 150.00)

        # Usamos Decimal para exactitud en el DSS de Norvin
        precio = Decimal(str(precio_base)).quantize(Decimal('0.01'))
        
        # ENTREGAMOS LA TUPLA
        yield (nombre, precio)