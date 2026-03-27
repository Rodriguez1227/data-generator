import random
from datetime import datetime, timedelta

def generate_citas(n, cliente_ids):
    """
    Generador puro de citas.
    n: Cantidad de registros a generar.
    cliente_ids: Lista de IDs de clientes ya cargada en memoria (Inyección de dependencias).
    """
    if not cliente_ids:
        # No imprimimos error aquí, lo manejamos en el orquestador
        return

    estados = ['Pendiente', 'Completada', 'Cancelada']
    descripciones = [
        'Revisión general', 
        'Cambio de aceite', 
        'Sonido extraño en motor', 
        'Ajuste de frenos',
        'Mantenimiento preventivo',
        'Cambio de llantas'
    ]

    for _ in range(n):
        id_cliente = random.choice(cliente_ids)
        # Generamos un rango de fechas (pasadas y futuras)
        fecha = datetime.now() + timedelta(days=random.randint(-60, 60))
        estado = random.choice(estados)
        # Formato de hora simple
        hora = f"{random.randint(8, 17):02d}:00:00"
        desc = random.choice(descripciones)
        
        # ENTREGAMOS LA TUPLA (Sin insertar aún)
        yield (id_cliente, fecha.date(), estado, hora, desc)