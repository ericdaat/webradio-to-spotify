import logging

from src import scraping
from src.spotify import SpotifyApi
from src.db import Session, Song


class Updater(object):
    def __init__(self):
        self.spotify = SpotifyApi()
        self.is_authenticated = False

        # Add new scrapers here
        self.scrapers = [
            scraping.KSHEScraper(),
            scraping.EagleScraper(),
        ]

    def spotify_auth(self):
        """Authenticates using Authorization Code Flow.

        Returns:
            str: URL to redirect to
        """
        url = self.spotify._authorization_code_flow_authentication()

        return url

    def spotify_callback(self, authorization_code):
        """Function called by Spotify with access token in the request
        parameters.

        Args:
            authorization_code (str): Authorization code
        """
        response = self.spotify._client_credentials_authentication(
            authorization_code
        )

        self.spotify._access_token = response['access_token']
        self.spotify._token_type = response['token_type']
        self.spotify._token_expires_in = response['expires_in']

        if response.get('access_token'):
            # TODO: add authenticated until timestamp
            self.is_authenticated = True

    def search_songs_in_spotify(self, radio_history):
        """Retrieve songs informations from title and artist using Spotify
        Search API.

        Args:
            radio_history (list(dict)): list of dict with title and \
                artist as keys

        Returns:
            list(dict): list of dict of spotify songs
        """
        spotify_songs = [self.spotify.search_track(s['title'], s['artist'])
                         for s in radio_history if 'title' in s]

        spotify_songs = [s for s in spotify_songs if 'spotify_uri' in s]

        return spotify_songs

    def filter_and_save_songs_to_db(self, spotify_songs,
                                    scraper_name, playlist_id):
        """Filter out songs that have already been added and add the
        remaining songs to the playlist.

        Args:
            spotify_songs (list(dict)): List of spotify songs as dict
            scraper_name (str): Scraper class name

        Returns:
            list(dict): List of spotify songs that are not in the playlist yet
        """
        # save tracks in DB
        session = Session()
        spotify_filtered_songs = []

        for i, song in enumerate(spotify_songs):
            # Don't save and upload song if it exists
            match = session.query(Song)\
                           .filter_by(
                               spotify_uri=song['spotify_uri'],
                               playlist_id=playlist_id
                            )\
                           .first()

            if match is None:
                song["scraper_name"] = scraper_name
                song["playlist_id"] = playlist_id
                session.add(Song(**song))
                spotify_filtered_songs.append(song)
            else:
                logging.warning('{0} already in playlist'
                                .format(song['song_name']))

        session.commit()

        return spotify_filtered_songs

    def add_songs_to_playlist(self, spotify_songs, playlist_id):
        """Add spotify songs to a playlist, using songs URI.

        Args:
            spotify_songs (list(dict)): List of spotify songs

        Returns:
            json: Json response from the Spotify API
        """
        logging.info('will add {0} tracks'.format(len(spotify_songs)))

        response = self.spotify.add_tracks_to_playlist(
            [s['spotify_uri'] for s in spotify_songs],
            playlist_id
        )

        return response

    def scrap_and_update(self):
        """Run the whole pipeline for every scraper:

        - Scrap the concerned website and get their song history
        - Search for the songs in Spotify
        - Filter the songs already in playlist and save them to DB
        - Add the filtered songs to the playlist

        Returns:
            list(dict): Inserted songs
        """
        inserted_songs = []
        n_inserted_songs = 0

        for scraper in self.scrapers:
            # get song history
            song_history = scraper.get_song_history()

            # spotify songs
            spotify_songs = self.search_songs_in_spotify(song_history)

            # filter out already present songs and sync database
            spotify_filtered_songs = self.filter_and_save_songs_to_db(
                spotify_songs,
                scraper_name=scraper.name,
                playlist_id=scraper.playlist_id
            )

            # upload the filtered out songs to the spotify playlist
            _ = self.add_songs_to_playlist(
                spotify_filtered_songs,
                playlist_id=scraper.playlist_id
            )

            inserted_songs.append(
                {
                    "scraper": scraper.name,
                    "playlist_id": scraper.playlist_id,
                    "songs": spotify_filtered_songs
                }
            )

            n_inserted_songs += len(spotify_filtered_songs)

        return inserted_songs, n_inserted_songs
