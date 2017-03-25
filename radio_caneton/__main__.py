from apscheduler.schedulers.blocking import BlockingScheduler

from . import radio_caneton


def update_db():
    pass

scheduler = BlockingScheduler()
scheduler.add_job(update_db, 'interval', seconds=5)
scheduler.start()
