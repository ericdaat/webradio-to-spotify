import unittest

from src.scraping import KSHEScraper


class TestKSHEScraper(unittest.TestCase):
    def test_get_song_history(self):
        scraper = KSHEScraper()

        history = scraper.get_song_history()
        self.assertIsInstance(history, list)
        self.assertTrue(len(history) > 0)

        history_item = history[0]
        self.assertIsInstance(history_item, dict)
        self.assertIn("title", history_item)
        self.assertIn("artist", history_item)
        self.assertIn("timestamp", history_item)
