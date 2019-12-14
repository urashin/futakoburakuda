from flask import Flask, request, jsonify
import werkzeug
from flask_cors import CORS
from translator.Translator import Translator

app = Flask(__name__)
CORS(app)

trans = Translator()

@app.route("/transform", methods=["POST"])
def transform():
    content = request.json
    text = content['text']

    print(text)

    # テキストデータを変換する処理
    translated_text = trans.translate(text, type='jk')
    print(translated_text)

    if len(translated_text) == 0:
        return jsonify({"text": text})

    return jsonify({"text": translated_text})


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print(e)
    return 'bad request!', 400


@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_bad_request(e):
    print(e)
    return 'Internal Server error!', 500
