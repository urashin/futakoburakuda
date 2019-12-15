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
    filterMode = content['filterMode']

    print(text)
    print("mode:{}".format(filterMode))

    # テキストデータを変換する処理
    trans = Translator()
    translated_text = trans.translate(text, type=filterMode)
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
