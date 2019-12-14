from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/transform", methods=["POST"])
def transform():
    content = request.json
    img = content['img']
    return jsonify({"img": img})