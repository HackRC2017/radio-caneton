import json
import os

import requests


RC_AUTH_KEY = os.environ.get('RC_AUTH_KEY')
THEMES_BLACKLIST = [14, 16, 21, 23]


def get_lineup_articles(href, max_depth=5):
    if max_depth == 0:
        return []
    articles = []
    lineup_r = requests.get(href)
    for article in lineup_r.json()['pagedList']['items']:
        headers = {'Authorization': RC_AUTH_KEY}
        if article['contentType']['name'] == 'Nouvelle':
            article_r = requests.get(article['selfLink']['href'], headers=headers)
            articles.append(article_r.json())
    if lineup_r.json()['pagedList'].get('nextPageLink'):
        next_page = lineup_r.json()['pagedList']['nextPageLink']['href']
        articles.extend(get_lineup_articles(next_page, max_depth-1))
    return articles


def get_articles():
    articles = []
    with open('themes.json') as f:
        themes = json.load(f)['themes']
    for theme in themes:
        if theme['id'] not in THEMES_BLACKLIST:
            articles.extend(get_lineup_articles(theme['lineupLink']['href']))
    return articles
