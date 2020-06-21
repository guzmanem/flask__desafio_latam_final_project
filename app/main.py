import flask
from flask import request, jsonify

app = flask.Flask(__name__)

@app.route('/api/v1/', methods=['POST'])
def home():
   return jsonify(request.json)
