from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
from flask_socketio import SocketIO , emit , send
from datetime import datetime, date
import numpy as np
import os
import time
import requests
import cv2
import face_recognition





TIEMPO_ESPERA_SEG = 0.5
nombre_muestra = 'gil'


app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("mostrar_valor")
def handle_mostrar_valor():
    emit("muestra", {"nombre_muestra": nombre_muestra})


if __name__ == "__main__":
    socketio.run(app, port=8000, debug=True)




