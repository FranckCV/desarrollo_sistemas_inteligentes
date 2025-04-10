

# # Bucle infinito (podés frenarlo con Ctrl+C)
# while True:
#     try:
#         # Capturar imagen
#         response = requests.get(esp32_url)
        
#         if response.status_code == 200:
#             # Nombre con marca de tiempo
#             now = datetime.now().strftime("%Y%m%d_%H%M%S")
#             file_name = f"foto_{now}.jpg"
            
#             # Guardar imagen local
#             with open(file_name, 'wb') as f:
#                 f.write(response.content)
            
#             print(f"[✔] Imagen guardada: {file_name}")
#         else:
#             print("[✘] Error al capturar imagen, código:", response.status_code)
    
#     except Exception as e:
#         print("[✘] Error:", e)
    
#     # Esperar 5 segundos
#     time.sleep(5)


import face_recognition
import cv2
import os
import time
from datetime import datetime
import requests

DIRECCION_IP = '192.168.114.181'

esp32_url = f'http://{DIRECCION_IP}/capture'


rostros_conocidos = []
nombres = []

for archivo in os.listdir("muestras"):
    imagen = face_recognition.load_image_file(f"rostros/{archivo}")
    encoding = face_recognition.face_encodings(imagen)
    if encoding:
        rostros_conocidos.append(encoding[0])
        nombres.append(os.path.splitext(archivo)[0])

# Loop: toma foto cada 5 segundos y hace reconocimiento
while True:
    try:
        response = requests.get(esp32_url)
        if response.status_code == 200:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"fotos/foto_{now}.jpg"
            with open(nombre_archivo, 'wb') as f:
                f.write(response.content)
            print(f"[✔] Foto guardada: {nombre_archivo}")

            # Procesar la imagen
            imagen = face_recognition.load_image_file(nombre_archivo)
            ubicaciones = face_recognition.face_locations(imagen)
            codificaciones = face_recognition.face_encodings(imagen, ubicaciones)

            for (top, right, bottom, left), encoding in zip(ubicaciones, codificaciones):
                # Comparar con rostros conocidos
                coincidencias = face_recognition.compare_faces(rostros_conocidos, encoding)
                nombre = "Desconocido"

                if True in coincidencias:
                    idx = coincidencias.index(True)
                    nombre = nombres[idx]

                print(f"➡ Cara detectada: {nombre}")
        
        else:
            print(f"[✘] Fallo al capturar imagen (status {response.status_code})")

    except Exception as e:
        print(f"[✘] Error: {e}")

    # Esperar 5 segundos
    time.sleep(5)







