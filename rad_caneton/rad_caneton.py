import copy
import itertools
import json
import os
import random

from apscheduler.schedulers.background import BackgroundScheduler
import pymongo
import requests


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(rad_can.get_new_articles, 'interval', minutes=5)



RC_AUTH_KEY = os.environ.get('RC_AUTH_KEY')

client = pymongo.MongoClient()
db = client.articles

_articles = []
ARTICLES_FILE = 'articles.json'
THEMES_BLACKLIST = [14, 16, 21, 23]


def _is_valid_article(article):
    if article['contentType']['name'] == 'Nouvelle':
        return True
    return False


def load_articles(number=100, from_file=False):
    global _articles
    if from_file and os.path.isfile(ARTICLES_FILE):
        with open(ARTICLES_FILE) as f:
            _articles = json.load(f)
        return len(_articles)
    themes = _get_theme_lineups()
    loaded_number = 0
    for i in itertools.cycle(range(len(themes))):
        try:
            _articles.append(next(themes[i]['generator']))
            loaded_number += 1
            print(loaded_number)
        except StopIteration:
            themes[i]['generator'] = _get_theme_articles(themes[i]['href'])
        if len(_articles) == number:
            break
        if not list(filter(lambda x: x is not None, themes)):
            break
    with open(ARTICLES_FILE, 'w') as f:
        json.dump(_articles, f)
    return loaded_number


def _get_theme_articles(href):
    lineup_r = requests.get(href)
    for article in lineup_r.json()['pagedList']['items']:
        headers = {'Authorization': RC_AUTH_KEY}
        if article['contentType']['name'] == 'Nouvelle':
            article_r = requests.get(article['selfLink']['href'], headers=headers)
            article = article_r.json()
            yield article
    if lineup_r.json()['pagedList'].get('nextPageLink'):
        yield from _get_theme_articles(lineup_r.json()['pagedList']['nextPageLink']['href'])


def _get_theme_lineups():
    theme_lineups = []
    with open('themes.json') as f:
        themes = json.load(f)['themes']
    random.shuffle(themes)
    themes = [t for t in themes if t['id'] not in THEMES_BLACKLIST]
    for theme in themes:
        theme_lineups.append({
            'href': theme['lineupLink']['href'],
            'generator': _get_theme_articles(theme['lineupLink']['href']),
        })
    return theme_lineups


def get_articles(number):
    global _articles
    if not _articles:
        load_articles(number=number, from_file=False)
    articles = _articles[:number]
    _articles = _articles[number:]
    return articles
