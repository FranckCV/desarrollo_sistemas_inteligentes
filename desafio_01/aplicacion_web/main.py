from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
from flask_socketio import SocketIO , emit , send
from datetime import datetime, date
import numpy as np
import os
import time
import requests
import cv2
import face_recognition
import controladores.controlador as controlador


DIRECCION_IP = '192.168.254.51'
ESP32_URL = f'http://{DIRECCION_IP}'
ESP32_URL_CAPTURE = f'{ESP32_URL}/capture'
ESP32_URL_STREAM = f'{ESP32_URL}:81/stream'

BASE_DIR = os.path.dirname(__file__)
MUESTRAS_DIR = os.path.join(BASE_DIR, "static/muestras")
CAPTURAS_DIR = os.path.join(BASE_DIR, "capturas")

os.makedirs(MUESTRAS_DIR, exist_ok=True)
os.makedirs(CAPTURAS_DIR, exist_ok=True)

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

encodings_muestras, nombres_muestras = cargar_muestras()

if not encodings_muestras:
    print("[✘] No se detectaron rostros en las muestras. Abortando.")
    exit()

print(f"[✔] Total de muestras válidas: {len(encodings_muestras)}\n")


TIEMPO_ESPERA_SEG = 1


app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)


@app.context_processor
def inject_globals():
    return dict(
            ESP32_URL_STREAM = ESP32_URL_STREAM ,
        )


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/")
@app.route("/stream")
def stream():
    return render_template("stream.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/add_photo")
def add_photo():
    per_id = request.cookies.get('per_id')
    return render_template("add_photo.html" , per_id = per_id)


@app.route("/guardar_persona", methods=["POST"])
def guardar_persona():
    try:
        resp = make_response(redirect(url_for('add_photo')))
        nombre = request.form["nombre"]

        per_id = controlador.insertar_persona(nombre)
        print(per_id)
        resp.set_cookie('per_id', str(per_id))
        return resp
    except Exception as e:
        return redirect(url_for('index'))


@app.route("/terminar_guardar", methods=["POST"])
def terminar_guardar():
    try:
        encodings_muestras, nombres_muestras = cargar_muestras()

        if not encodings_muestras:
            print("[✘] No se detectaron rostros en las muestras. Abortando.")
            exit()

        print(f"[✔] Total de muestras válidas: {len(encodings_muestras)}\n")

        return redirect(url_for('stream'))
    except Exception as e:
        return redirect(url_for('add'))


ultimo_nombre_detectado = None


@socketio.on("mostrar_valor")
def handle_mostrar_valor():
    global ultimo_nombre_detectado

    try:
        response = requests.get(ESP32_URL_CAPTURE, timeout=5)

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

                        nom_archivo = str(nombre)+'.jpg'
                        print('archivo encontrado',nom_archivo)
                        data_persona = controlador.obtener_persona_por_img(str(nom_archivo))
                        print('persona encontrado',data_persona)
                        id_per = data_persona[0] or 0
                        data_img_pri = controlador.obtener_img_principal_por_id(id_per)
                        print('nombre_img_pri',data_img_pri)

                        emit("muestra", {"nombre_muestra": nombre})
                        emit("persona", {"data_persona": data_persona})
                        emit("img_pri", {"data_img": data_img_pri})
                        ultimo_nombre_detectado = nombre

        else:
            print(f"[✘] Error HTTP: {response.status_code}")

    except Exception as e:
        print(f"[✘] Error: {e}")


def guardar(per_id):
    try:
        response = requests.get(ESP32_URL_CAPTURE)

        if response.status_code == 200:
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            # Validar detección de rostro
            face_locations = face_recognition.face_locations(frame)

            if not face_locations:
                print("[✘] No se detectó ningún rostro. Imagen no guardada.")
                # raise Exception("No se detectó ningún rostro en la imagen")
            else:
                # Guardar si hay al menos un rostro
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"foto_{per_id}_{now}.jpg"
                save_path = os.path.join(MUESTRAS_DIR, filename)

                cv2.imwrite(save_path, frame)
                print(f"[✔] Imagen guardada en: {save_path}")

                controlador.insertar_foto(filename, per_id)
                print(f"[✔] Imagen registrada en BD.")

        else:
            raise Exception(f"Error al capturar imagen: {response.status_code}")
    
    except Exception as e:
        print("[✘] Error al guardar imagen:", e)
        raise e  # Propagamos el error para que lo capture el endpoint

    time.sleep(TIEMPO_ESPERA_SEG)


@socketio.on("guardar_y_actualizar")
def handle_guardar_y_actualizar(data):
    per_id = data.get("per_id")

    guardar(per_id)  # Intenta guardar solo si hay rostro (tu función ya lo hace)

    # Luego de guardar (o fallar), consultar la lista actual de fotos
    lista_fotos = controlador.obtener_imgs_por_id(per_id)

    # Emitir lista al cliente
    emit("lista_fotos", {"fotos": lista_fotos})



@app.route("/api/guardar_foto", methods=["POST"])
def api_guardar_foto():
    try:
        per_id = request.json.get("per_id")
        guardar(per_id)

        latest_filename = sorted(os.listdir(MUESTRAS_DIR))[-1]
        return jsonify({"status": "ok", "filename": latest_filename})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})




if __name__ == "__main__":
    socketio.run(app, port=8000, debug=True)




