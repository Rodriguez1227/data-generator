import random
from faker import Faker

fake = Faker(['es_ES'])

def generate_proveedores(n):
    """
    Generador de proveedores.
    n: Cantidad total de registros (incluye los base).
    """
    # Proveedores fijos de Casa Tuning
    proveedores_base = [
        ('Repuestos El Rayo', '2222-5555', 'contacto@elrayo.com'),
        ('Distribuidora Total Moto', '2222-9999', 'ventas@totalmoto.com'),
        ('Accesorios ProTuning', '2222-0000', 'info@protuning.com')
    ]

    for i in range(n):
        if i < len(proveedores_base):
            nombre, tel, correo = proveedores_base[i]
        else:
            # Generación sintética para grandes volúmenes
            nombre = f"{random.choice(['Importadora', 'Multi-Repuestos', 'Suministros'])} {fake.company()}"
            tel = f"22{random.randint(10, 99)}-{random.randint(1000, 9999)}"
            correo = fake.unique.company_email()
        
        # ENTREGAMOS LA TUPLA
        # El motor (DBWriter) se encargará de ignorar duplicados si es necesario
        yield (nombre, tel, correo)