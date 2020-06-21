# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def cronjob():
   """
   Main cron job.
   The main cronjob to be run continuously.
   """
   print("Cron job is running")
   print("Tick! The time is: %s" % datetime.now())

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(cronjob, "interval", seconds=30)

scheduler.start()