import random

def get_random_moto():
    marcas = {
        "Yamaha": ["YZF-R3", "MT-07", "MT-09", "FZ25", "Crypton"],
        "Honda": ["CB125S", "CB190R", "CBR600RR", "XR150L", "Twister"],
        "Suzuki": ["Gixxer 150", "GSX-S750", "V-Strom 650", "AX100"],
        "Kawasaki": ["Ninja 400", "Z400", "Versys 650", "KLX 150"],
        "KTM": ["Duke 200", "Duke 390", "RC 200", "Adventure 390"]
    }
    marca = random.choice(list(marcas.keys()))
    modelo = random.choice(marcas[marca])
    return marca, modelo

def generate_plate():
    # Genera una placa estilo M 123456 o similar
    letras = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    return f"{random.choice(letras)}{random.choice(letras)}{random.randint(100, 999)}"