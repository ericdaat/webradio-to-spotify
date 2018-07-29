from bs4 import BeautifulSoup
import requests
import json
from operator import itemgetter
import logging


class KSHEScraper(object):
    def __init__(self, player_url):
        self.player_url = player_url
        logging.info('using {0}'.format(self.player_url))

    def get_song_history(self):
        soup = BeautifulSoup(requests.get(self.player_url).text, 'html.parser')
        song_history = soup.find('section', {'id': ['songHistory']})
        song_history_json = json.loads(
            song_history.find('script').text.split(';')[0].split('var songs = ')[-1]
        )
        song_history_json.sort(key=itemgetter('timestamp'))

        return song_history_json
