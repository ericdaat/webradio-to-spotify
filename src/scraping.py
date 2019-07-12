import logging
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from selenium import webdriver


class Scraper(ABC):
    def __init__(self, player_url):
        self.name = self.__class__.__name__
        self.player_url = player_url

        logging.info('Scraper initialized. Using {0}'.format(self.player_url))

    def scrap_webpage(self):
        """Scrap the webpage. This function must be called first in the
        ``get_song_history`` implementation.

        Returns:
            tuple: soup and driver
        """
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)

        driver.get(self.player_url)
        soup = BeautifulSoup(driver.page_source, "lxml")

        return soup, driver

    @abstractmethod
    def get_song_history(self):
        """Scrap the website and get its song history.
        This function must be overiden. Its implementation must return
        a list of dict with the following keys:

        - title
        - artist
        - timestamp (can be null, it's not used so far)
        """
        pass


class KSHEScraper(Scraper):
    def __init__(self):
        player_url = 'https://live.kshe95.com/listen/?'\
                     'utm_source=station-website&utm_medium=widget'\
                     '&utm_campaign=now-playing'

        super(KSHEScraper, self).__init__(player_url)

    def get_song_history(self):
        soup, driver = self.scrap_webpage()

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

        driver.quit()

        return history


class EagleScraper(Scraper):
    def __init__(self):
        player_url = 'https://eagle969.radio.com/playlist'

        super(EagleScraper, self).__init__(player_url)

    def get_song_history(self):
        soup, driver = self.scrap_webpage()

        recently_played = soup.find_all("div", {"class": "ts-track-item"})

        history = []

        for recently_played_item in recently_played:
            title = recently_played_item.find(
                "div",
                {"class": "ts-song-title tagstation__song"}
            ).text.strip().lower()

            artist = recently_played_item.find(
                "div",
                {"class": "ts-artist tagstation__artist"}
            ).text.strip().lower()

            history.append(
                {"title": title, "artist": artist, "timestamp": None}
            )

        driver.quit()

        return history
