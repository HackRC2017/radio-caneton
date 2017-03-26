import datetime
import json
import logging
import os

import pymongo
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from . import radio_caneton as rc


logging.getLogger().setLevel(logging.INFO)

OBAMO_HOST = os.environ.get('OBAMO_HOST')

MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = os.environ.get('MONGODB_PORT', 27017)
MONGODB_DB = os.environ.get('MONGODB_DB', 'tempo')

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DB]


def escape_keys(original):
    if isinstance(original, dict):
        return {k.replace('$', '_'): escape_keys(v) for k,v in original.items()}
    elif isinstance(original, list):
        return [escape_keys(item) for item in original]
    else:
        return original


def update_db():
    logging.info('updating db')
    articles_added = 0
    obamo_json_errors = 0
    articles = rc.get_articles()
    for article in articles:
        if db.articles.find_one({'id': article['id']}):
            logging.info(f'article {article["id"]} already in db')
            continue
        logging.info(f'getting obamo: {article["selfLink"]["href"]}')
        r = requests.post(f'http://{OBAMO_HOST}/readtime',
                          json={'url': article['selfLink']['href']})
        try:
            obamo_json = r.json()
        except json.decoder.JSONDecodeError:
            logging.info('got bad obamo json response')
            obamo_json_errors += 1
            continue
        article['readTime'] = obamo_json
        db.articles.insert_one(escape_keys(article))
        logging.info(f'added article {article["id"]} to db')
        articles_added += 1
    db.stats.insert_one({
        'datetime': str(datetime.datetime.now()),
        'articles_added': articles_added,
        'articles_fetched': len(articles),
        'obamo_json_errors': obamo_json_errors,
    })


update_db()


scheduler = BlockingScheduler()
scheduler.add_job(update_db, 'interval', minutes=5)
scheduler.start()
