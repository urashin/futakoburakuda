from flask import Flask, request, jsonify
import werkzeug
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/transform", methods=["POST"])
def transform():
    content = request.json
    text = content['text']

    print(text)

    # テキストデータを変換する処理

    return jsonify({"text": text})


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print(e)
    return 'bad request!', 400


@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_bad_request(e):
    print(e)
    return 'Internal Server error!', 500
