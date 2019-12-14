from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from create_image import *

app = Flask(__name__)
CORS(app)


@app.route("/transform", methods=["POST"])
def transform():
    content = request.json
    url = content['url']
    print(url)

    alt = content['alt']
    alts = parse_alt(alt)
    print(alts)

    img_path = generate_file_path(url)
    print(img_path)

    crt_img = create_image()
    crt_img.create(alts, img_path)

    return jsonify({"imgPath": img_path})


def parse_alt(alt):
    print(alt)
    alts = alt.replace("画像に含まれている可能性があるもの:", "").split('、')
    return alts


def generate_file_path(url):
    h = hashlib.sha256()
    h.update(url.encode('utf-8'))
    file_path = './img/' + h.hexdigest() + '.jpg'
    return file_path
