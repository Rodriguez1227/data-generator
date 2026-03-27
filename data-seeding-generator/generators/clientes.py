from faker import Faker

# Usamos localización en español para nombres y datos más realistas
fake = Faker(['es_ES'])

def generate_clientes(n):
    """
    Generador puro de datos de clientes.
    n: Cantidad de registros a fabricar.
    """
    for _ in range(n):
        nombre = fake.first_name()
        apellido = fake.last_name()
        
        # Generación de teléfono (formato Nicaragua 8 dígitos)
        telefono = str(fake.random_int(70000000, 89999999))
        
        # Usamos .unique para evitar colisiones en correos si n es muy grande
        correo = fake.unique.email()
        
        # Limitar a 50 caracteres según tu restricción de DB
        direccion = fake.address().replace("\n", ", ")[:50] 
        
        # Generar usuario único basado en el nombre
        usuario = f"{nombre.lower()}{fake.random_int(100, 999)}"
        
        # En una versión avanzada, aquí podrías usar un hash real si fuera necesario
        password = "hashed_password_example" 
        
        # El IdRol lo dejamos configurable o fijo según tu lógica de negocio
        id_rol = 3  # Rol de Cliente
        
        # ENTREGAMOS LA TUPLA
        # El orden debe coincidir con el que pida el orquestador/db_writer
        yield (
            nombre, 
            apellido, 
            telefono, 
            correo, 
            direccion, 
            usuario, 
            password, 
            id_rol
        )