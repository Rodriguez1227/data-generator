import random
from faker import Faker

fake = Faker(['es_ES'])

def generate_usuarios(n):
    """
    Generador de usuarios (Personal del taller).
    n: Cantidad total de usuarios a generar (mínimo 3 para cubrir los roles base).
    """
    # Usuarios base críticos para el funcionamiento de las pruebas de Norvin
    usuarios_base = [
        ('Admin', 'Principal', '88889999', 'admin@casatuning.com', 'admin', 'password123', 1),
        ('Carlos', 'Mecánico', '77778888', 'carlos@casatuning.com', 'tecnico1', 'mecanico123', 2),
        ('José', 'Mecánico', '55554444', 'jose@casatuning.com', 'tecnico2', 'mecanico123', 2)
    ]

    for i in range(n):
        if i < len(usuarios_base):
            # Entregamos primero los usuarios reales necesarios
            yield usuarios_base[i]
        else:
            # Generación sintética para staff adicional
            nombre = fake.first_name()
            apellido = fake.last_name()
            tel = str(fake.random_int(70000000, 89999999))
            correo = fake.unique.email()
            user_login = f"{nombre.lower()[:3]}{random.randint(100, 999)}"
            password = "hashed_staff_password"
            
            # Asignamos roles aleatorios entre Técnico (2) y Recepción/Otros (3+)
            id_rol = random.randint(2, 3)
            
            yield (nombre, apellido, tel, correo, user_login, password, id_rol)