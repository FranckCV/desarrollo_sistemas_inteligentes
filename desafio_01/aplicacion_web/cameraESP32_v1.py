

import os
import time
from datetime import datetime
import requests

DIRECCION_IP = '192.168.1.113'

esp32_url = f'http://{DIRECCION_IP}/capture'


# Bucle infinito (podés frenarlo con Ctrl+C)
while True:
    try:
        # Capturar imagen
        response = requests.get(esp32_url)
        
        if response.status_code == 200:
            # Nombre con marca de tiempo
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"foto_{now}.jpg"
            
            # Guardar imagen local
            with open(file_name, 'wb') as f:
                f.write(response.content)
            
            print(f"[✔] Imagen guardada: {file_name}")
        else:
            print("[✘] Error al capturar imagen, código:", response.status_code)
    
    except Exception as e:
        print("[✘] Error:", e)
    
    # Esperar 5 segundos
    time.sleep(5)




