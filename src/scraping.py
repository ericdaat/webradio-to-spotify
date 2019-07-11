import logging
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from selenium import webdriver


class Scraper(ABC):
    def __init__(self, player_url):
        self.name = self.__class__.__name__
        self.player_url = player_url

        options = webdriver.FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        logging.info('Scraper initialized. Using {0}'.format(self.player_url))

    @abstractmethod
    def get_song_history(self):
        pass


class KSHEScraper(Scraper):
    def __init__(self):
        player_url = 'https://live.kshe95.com/listen/?'\
                     'utm_source=station-website&utm_medium=widget'\
                     '&utm_campaign=now-playing'

        super(KSHEScraper, self).__init__(player_url)

    def get_song_history(self):
        self.driver.get(self.player_url)
        soup = BeautifulSoup(self.driver.page_source, "lxml")

        recently_played = soup.find_all("li", {"class": "hll-recent-track"})

        history = []

        for recently_played_item in recently_played:
            # get song infos
            song_results = recently_played_item.find_all(
                "a",
                {"class": "hll-link-color-hover ember-view"}
            )
            title, artist = [r.text.strip().lower() for r in song_results]

            # get song played time
            song_timestamp = recently_played_item.find(
                "div",
                {"class": "time"}
            ).time["datetime"]

            history.append(
                {"title": title, "artist": artist, "timestamp": song_timestamp}
            )

        return history
