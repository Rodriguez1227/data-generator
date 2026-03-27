import random
from services.db_writer import get_ids_from_db

def generate_motos(n, cli_ids):
    """
    Genera datos de motos asegurando que las placas sean únicas 
    comparándolas con las ya existentes en la base de datos.
    """
    # 1. Obtener placas existentes para evitar colisiones
    try:
        raw_plates = get_ids_from_db("SELECT Placa FROM Motos")
        # Limpiamos los datos para tener un set de strings: {'M 123', 'M 456'}
        existing_plates = set(r[0] if isinstance(r, (list, tuple)) else r for r in raw_plates)
    except:
        existing_plates = set()

    marcas = ['Honda', 'Yamaha', 'Suzuki', 'Kawasaki', 'KTM', 'Bajaj', 'Genesis']
    modelos = {
        'Honda': ['CB125S', 'CB190R', 'Africa Twin', 'Shadow'],
        'Yamaha': ['YZF-R3', 'MT-07', 'FZ-S', 'XTZ 125'],
        'Suzuki': ['Gixxer 150', 'V-Strom 650', 'GN 125'],
        'Kawasaki': ['Ninja 400', 'Z900', 'KLR 650'],
        'Bajaj': ['Pulsar NS200', 'Dominar 400', 'Platina 100']
    }
    colores = ['Negro Matte', 'Rojo Racing', 'Azul Eléctrico', 'Blanco Perla', 'Verde Kawasaki']

    motos_data = []
    placas_generadas_en_lote = set()

    for i in range(n):
        # Asignamos una moto por cada cliente del lote (o aleatorio si sobran)
        id_cliente = cli_ids[i % len(cli_ids)]
        
        # --- GENERACIÓN DE PLACA ÚNICA ---
        intentos = 0
        while True:
            # Formato: M + 6 dígitos aleatorios (como en tu error de SQL)
            nueva_placa = f"M {random.randint(10000, 999999)}"
            
            # Verificamos que no esté en la DB ni se haya generado en este mismo ciclo
            if nueva_placa not in existing_plates and nueva_placa not in placas_generadas_en_lote:
                placas_generadas_en_lote.add(nueva_placa)
                break
            
            intentos += 1
            if intentos > 1000: # Seguridad para evitar bucle infinito
                nueva_placa = f"M {random.randint(1000000, 9999999)}" 
                break

        marca = random.choice(marcas)
        modelo = random.choice(modelos.get(marca, ['Universal Custom']))
        anio = random.randint(2015, 2026)
        color = random.choice(colores)

        motos_data.append((
            id_cliente, 
            nueva_placa, 
            marca, 
            modelo, 
            anio, 
            color
        ))

    return motos_data