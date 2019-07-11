import logging
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver


class KSHEScraper(object):
    def __init__(self):
        self.player_url = 'https://live.kshe95.com/listen/?'\
                          'utm_source=station-website&utm_medium=widget'\
                          '&utm_campaign=now-playing'
        logging.info('using {0}'.format(self.player_url))

    def get_song_history(self):
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)

        driver.get(self.player_url)
        soup = BeautifulSoup(driver.page_source, "lxml")

        recently_played = soup.find_all("li", {"class": "hll-recent-track"})

        history = []

        for recently_played_item in recently_played:
            # get song infos
            song_results = recently_played_item.find_all(
                "a",
                {"class": "hll-link-color-hover ember-view"}
            )
            title, artist = [r.text.strip() for r in song_results]

            # get song played time
            song_timestamp = recently_played_item.find(
                "div",
                {"class": "time"}
            ).time["datetime"]
            song_timestamp = datetime.fromisoformat(song_timestamp)

            history.append(
                {"title": title, "artist": artist, "timestamp": song_timestamp}
            )

        return history
