from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app.route("/transform", methods=["POST"])
def transform():
    content = request.json
    url = content['url']
    print(url)

    alt = content['alt']
    alts = parse_alt(alt)
    print(alts)

    # TODO: 属性ワードを画像生成ライブラリに渡す

    img_path = ""
    return jsonify({"imgPath": img_path})


def parse_alt(alt):
    print(alt)
    alts = alt.replace("画像に含まれている可能性があるもの:", "").split('、')
    return alts
