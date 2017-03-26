import datetime
import json
import os

import pymongo
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from . import radio_caneton as rc


OBAMO_HOST = os.environ.get('OBAMO_HOST')

client = pymongo.MongoClient()
db = client.db


def escape_keys(original):
    if isinstance(original, dict):
        return {k.replace('$', '_'): escape_keys(v) for k,v in original.items()}
    elif isinstance(original, list):
        return [escape_keys(item) for item in original]
    else:
        return original


def update_db():
    articles_added = 0
    articles = rc.get_articles()
    for article in articles:
        if db.articles.find({'id': article['id']}):
            continue
        r = requests.post(f'http://{OBAMO_HOST}/readtime',
                          json={'url': article['selfLink']['href']})
        article['readTime'] = r.json()
        db.articles.insert_one(escape_keys(article))
        articles_added += 1
    db.stats.insert_one({
        'datetime': str(datetime.datetime.now()),
        'articles_added': articles_added,
    })


update_db()


scheduler = BlockingScheduler()
scheduler.add_job(update_db, 'interval', minutes=5)
scheduler.start()
