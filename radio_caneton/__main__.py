from apscheduler.schedulers.blocking import BlockingScheduler
import pymongo

from . import radio_caneton as rc


client = pymongo.MongoClient()
db = client.articles


def update_db():
    articles = rc.get_articles()


scheduler = BlockingScheduler()
scheduler.add_job(update_db, 'interval', minutes=5)
scheduler.start()
