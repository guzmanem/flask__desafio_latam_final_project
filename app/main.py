from apscheduler.schedulers.background import BackgroundScheduler
from flask import request, jsonify
import flask


def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")
    app.logger.info('test')

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',minutes=1)
sched.start()

app = flask.Flask(__name__)

@app.route('/api/v1/', methods=['POST'])
def home():
   return jsonify(request.json)
