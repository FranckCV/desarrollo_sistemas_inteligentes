import requests
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time

# Configuración
DIRECCION_IP = '192.168.1.113'  # Cambia a tu IP real del ESP32-CAM
ESP32_URL = f'http://{DIRECCION_IP}/capture'

BASE_DIR = os.path.dirname(__file__)
MUESTRAS_DIR = os.path.join(BASE_DIR, "muestras")
CAPTURAS_DIR = os.path.join(BASE_DIR, "capturas")

os.makedirs(MUESTRAS_DIR, exist_ok=True)
os.makedirs(CAPTURAS_DIR, exist_ok=True)

# Cargar imágenes de muestra
def cargar_muestras():
    encodings = []
    nombres = []

    print("[ℹ] Cargando muestras...")
    
    for filename in os.listdir(MUESTRAS_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(MUESTRAS_DIR, filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)
            
            if encoding:
                encodings.append(encoding[0])
                nombre = os.path.splitext(filename)[0]
                nombres.append(nombre)
                print(f"  [✔] Muestra cargada: {nombre}")
            else:
                print(f"  [✘] No se detectó rostro en: {filename}")
    
    return encodings, nombres

# Cargar muestras
encodings_muestras, nombres_muestras = cargar_muestras()

if not encodings_muestras:
    print("[✘] No se detectaron rostros en las muestras. Abortando.")
    exit()

print(f"[✔] Total de muestras válidas: {len(encodings_muestras)}\n")

# Bucle principal
while True:
    try:
        response = requests.get(ESP32_URL, timeout=10)
        
        if response.status_code == 200:
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            if not face_encodings:
                print("[❗] No se detectaron rostros en la imagen capturada.")
            else:
                for face_encoding in face_encodings:
                    nombre = "Desconocido"
                    matches = face_recognition.compare_faces(encodings_muestras, face_encoding, tolerance=0.5)

                    if True in matches:
                        idx = matches.index(True)
                        nombre = nombres_muestras[idx]
                    
                    print(f"[⚡] Rostro reconocido: {nombre}")

            # Guardar imagen capturada (opcional)
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta = os.path.join(CAPTURAS_DIR, f"foto_{now}.jpg")
            cv2.imwrite(ruta, frame)

        else:
            print(f"[✘] Error HTTP: {response.status_code}")

    except Exception as e:
        print(f"[✘] Error de captura o reconocimiento: {str(e)}")

    time.sleep(0.5)
