from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
from flask_socketio import SocketIO , emit , send
import numpy as np
import os
import requests
import cv2
import face_recognition


ESP32_URL = f'http://192.168.254.51/capture'

BASE_DIR = os.path.dirname(__file__)
MUESTRAS_DIR = os.path.join(BASE_DIR, "static/muestras")
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



TIEMPO_ESPERA_SEG = 0.5


app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


# Guardar último rostro detectado para evitar repeticiones innecesarias
ultimo_nombre_detectado = None

@socketio.on("mostrar_valor")
def handle_mostrar_valor():
    global ultimo_nombre_detectado

    try:
        response = requests.get(ESP32_URL, timeout=5)

        if response.status_code == 200:
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            if not face_encodings:
                print("[❗] No se detectaron rostros.")
                emit("muestra", {"nombre_muestra": "Desconocido"})
                ultimo_nombre_detectado = None
            else:
                for face_encoding in face_encodings:
                    nombre = "Desconocido"
                    matches = face_recognition.compare_faces(encodings_muestras, face_encoding, tolerance=0.5)

                    if True in matches:
                        idx = matches.index(True)
                        nombre = nombres_muestras[idx]

                    if nombre != ultimo_nombre_detectado:
                        print(f"[⚡] Rostro reconocido: {nombre}")
                        emit("muestra", {"nombre_muestra": nombre})
                        ultimo_nombre_detectado = nombre

        else:
            print(f"[✘] Error HTTP: {response.status_code}")

    except Exception as e:
        print(f"[✘] Error: {e}")


if __name__ == "__main__":
    socketio.run(app, port=8000, debug=True)




