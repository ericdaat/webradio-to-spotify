import logging

from src.scraping import KSHEScraper
from src.spotify import SpotifyApi
from src.db import Session, Song


class Updater(object):
    def __init__(self):
        self.radio_scraper = KSHEScraper()
        self.spotify = SpotifyApi()
        self.is_authenticated = False

    def spotify_auth(self):
        url = self.spotify._authorization_code_flow_authentication()

        return url

    def spotify_callback(self, authorization_code):
        response = self.spotify._client_credentials_authentication(
            authorization_code
        )

        self.spotify._access_token = response['access_token']
        self.spotify._token_type = response['token_type']
        self.spotify._token_expires_in = response['expires_in']

        if response.get('access_token'):
            self.is_authenticated = True

    def get_radio_history(self):
        radio_history = self.radio_scraper.get_song_history()

        return radio_history

    def search_songs_in_spotify(self, radio_history):
        spotify_songs = [self.spotify.search_track(s['title'], s['artist'])
                         for s in radio_history if 'title' in s]

        spotify_songs = [s for s in spotify_songs if 'spotify_uri' in s]

        return spotify_songs

    def filter_and_save_songs_to_db(self, spotify_songs):
        # save tracks in DB
        session = Session()
        for i, song in enumerate(spotify_songs):
            # Don't save and upload song if it exists
            if session.query(Song).filter_by(spotify_uri=song['spotify_uri']):
                spotify_songs.pop(i)
            else:
                session.add(Song(**song))
        session.commit()

        return spotify_songs

    def add_songs_to_playlist(self, spotify_songs):
        logging.info('will add {0} tracks'.format(len(spotify_songs)))

        response = self.spotify.add_tracks_to_playlist(
            [s['spotify_uri'] for s in spotify_songs]
        )

        return response
