from flask_crontab import Crontab
from flask import request, jsonify
import flask

app = flask.Flask(__name__)
crontab = Crontab(app)

@app.route('/api/v1/', methods=['POST'])
def home():
   return jsonify(request.json)

@crontab.job(minute="1", hour="0")
def my_scheduled_job():
   print('entrooo al job')
   app.logger.info('entro')