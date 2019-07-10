import json
import logging
from operator import itemgetter

from bs4 import BeautifulSoup
import requests


class KSHEScraper(object):
    def __init__(self):
        self.player_url = 'http://player.listenlive.co/20101/en/songhistory'
        logging.info('using {0}'.format(self.player_url))

    def get_song_history(self):
        soup = BeautifulSoup(requests.get(self.player_url).text, 'html.parser')
        song_history = soup.find('section', {'id': ['songHistory']})
        song_history_json = json.loads(
            song_history.find('script').text.split(';')[0].split('var songs = ')[-1]
        )
        song_history_json.sort(key=itemgetter('timestamp'))

        return song_history_json
