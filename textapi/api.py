from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/transform", methods=["POST"])
def transform():
    content = request.json
    text = content['text']
    return jsonify({"text": text})
