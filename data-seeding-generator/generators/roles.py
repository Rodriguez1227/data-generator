from services.db_writer import insert_data

def seed_roles():
    roles = [
        (1, 'Administrador'),
        (2, 'Tecnico'),
        (3, 'Cliente')
    ]
    # Usamos SET IDENTITY_INSERT porque IdRol es IDENTITY
    query = """
    IF NOT EXISTS (SELECT 1 FROM Roles WHERE IdRol = ?)
    BEGIN
        SET IDENTITY_INSERT Roles ON;
        INSERT INTO Roles (IdRol, NombreRol) VALUES (?, ?);
        SET IDENTITY_INSERT Roles OFF;
    END
    """
    for id_r, nombre in roles:
        insert_data(query, (id_r, id_r, nombre))
    print("✓ Roles verificados.")