from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
# from flask_jwt import JWT, jwt_required, current_identity
# import uuid
# from functools import wraps
import hashlib
import base64
from datetime import datetime, date


app = Flask(__name__, template_folder='templates')


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
