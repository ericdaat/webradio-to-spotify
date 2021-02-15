import unittest

from src import scraping


# Generic scraper test
class GenericScraperTest(unittest.TestCase):
    __test__ = False
    model = None

    @classmethod
    def setUpClass(cls):
        if cls is GenericScraperTest:
            raise unittest.SkipTest()

    def test_get_song_history(self):
        history = self.scraper.get_song_history()
        self.assertIsInstance(history, list)
        self.assertTrue(len(history) > 0)

        history_item = history[0]
        self.assertIsInstance(history_item, dict)
        self.assertIn("title", history_item)
        self.assertIn("artist", history_item)
        self.assertIn("timestamp", history_item)


# Add scrapers below for testing

class TestKSHEScraper(GenericScraperTest):
    scraper = scraping.KSHEScraper()


# class TestEagleScraper(GenericScraperTest):
#     scraper = scraping.EagleScraper()


# class TestQ1043Scrapper(GenericScraperTest):
#     scraper = scraping.Q1043Scrapper()


# class TestWMGKScrapper(GenericScraperTest):
#     scraper = scraping.WMGKScrapper()


# class TestKLOScrapper(GenericScraperTest):
#     scraper = scraping.KLOScrapper()
