""" Add new scrapers here. Please follow these steps to do so:

- Create a class whose names ends with `Scraper`, e.g: `YourScrapper`\
    (although it should be explicit which website it crawls).
- Make that class inherit from `Scraper`
- Call for `super()` in its constructor, and pass it the URL of the webpage\
    to crawl and the `playlist_id` to upload the songs to. e.g:

    .. code-block:: python

        player_url = 'https://radio.com/awesome-song-history'
        playlist_id = '3BCcE8T945z1MnfPWkFsfX'
        super(YourScrapper, self).__init__(player_url, playlist_id)

- Overide the `get_song_history` method, the first row should be:

    .. code-block:: python

        soup, driver = self.scrap_webpage()

- Add your scraper in the [tests](./tests/test_scraping.py) folder:

    .. code-block:: python

        class TestYourScraper(GenericScraperTest):
            scraper = scraping.YourScraper()

- Add your scraper in the
  [src.playlist_updater.Updater](./src/playlist_updater.py) class:

    .. code-block:: python

        self.scrapers = [
            scraping.KSHEScraper(),
            scraping.EagleScraper(),
            scraping.YourScraper()  # New scraper!
        ]

- You're all set!
"""

import logging
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from selenium import webdriver


class Scraper(ABC):
    def __init__(self, player_url, playlist_id):
        self.name = self.__class__.__name__
        self.player_url = player_url
        self.playlist_id = playlist_id

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
        playlist_id = '3BCcE8T945z1MnfPWkFsfX'

        super(KSHEScraper, self).__init__(player_url, playlist_id)

    def get_song_history(self):
        soup, driver = self.scrap_webpage()

        recently_played = soup.find_all("li", {"class": "hll-recent-track"})

        history = []

        for recently_played_item in recently_played:
            div = recently_played_item.find("div", {"class": "caption"})
            div = div.find("div", {"class": "vertical-align"})

            # get song infos
            h3 = div.find("h3")
            title = h3.find(
                "a",
                {"class": "hll-link-color-hover ember-view"}
            ).text.strip().lower()

            cite = div.find("cite")
            artist = cite.find(
                "a",
                {"class": "hll-link-color-hover ember-view"}
            ).text.strip().lower()

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
        playlist_id = '3BCcE8T945z1MnfPWkFsfX'

        super(EagleScraper, self).__init__(player_url, playlist_id)

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


class Q1043Scrapper(Scraper):
    def __init__(self):
        player_url = 'https://q1043.iheart.com/music/recently-played/'
        playlist_id = '3BCcE8T945z1MnfPWkFsfX'

        super(Q1043Scrapper, self).__init__(player_url, playlist_id)

    def get_song_history(self):
        soup, driver = self.scrap_webpage()

        recently_played = soup.find_all(
            "li",
            {"class": "playlist-track-container ondemand-track"}
        )

        history = []

        for recently_played_item in recently_played:
            title = recently_played_item.find(
                "a",
                {"class": "song-title"}
            ).text.strip().lower()

            artist = recently_played_item.find(
                "a",
                {"class": "artist-name"}
            ).text.strip().lower()

            history.append(
                {"title": title, "artist": artist, "timestamp": None}
            )

        driver.quit()

        return history
