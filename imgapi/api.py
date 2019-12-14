from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib

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

    file_path = generate_file_path(url)
    print(file_path)

    # TODO: ファイル名、属性ワードを画像生成ライブラリに渡して生成画像のパスを受け取る
    img_path = "hoge"

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
