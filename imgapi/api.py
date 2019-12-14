from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import hashlib
from pathlib import Path
import os
from create_image import *

app = Flask(__name__)
app.config["CLIENT_IMAGES"] = Path('./img').resolve()
CORS(app)


@app.route("/img/<image_name>", methods=["GET"])
def get_image(image_name):
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route("/transform", methods=["POST"])
def transform():
    content = request.json
    url = content['url']
    print(url)

    alt = content['alt']
    alts = parse_alt(alt)
    print(alts)

    img_name = generate_file_name(url)
    img_path = generate_file_path(img_name)
    print(img_path)

    crt_img = create_image()
    crt_img.create(alts, img_path)

    return jsonify({"imgName": img_name})


def parse_alt(alt):
    print(alt)
    alts = alt.replace("画像に含まれている可能性があるもの:", "").split('、')
    return alts


def generate_file_name(url):
    h = hashlib.sha256()
    h.update(url.encode('utf-8'))
    file_name = h.hexdigest() + '.jpg'

    return file_name

def generate_file_path(file_name):
    file_path = './img/' + file_name
    return file_path
