import json
import base64
import logging
from urllib.parse import urlencode

import requests


class SpotifyApi(object):
    def __init__(self):
        # Load credentials
        with open(".spotify-token.json") as f:
            credentials = json.loads(f.read())

        self._user_id = credentials['user_id']
        self._client_id = credentials['client_id']
        self._client_secret = credentials['client_secret']
        self.redirect_uri = credentials['redirect_uri']

        # Will be set after spotify auth
        self._access_token = None
        self._refresh_token = None
        self._token_expires_in = None
        self._token_type = None

    def _client_credentials_authentication(self, authorization_code=None):
        auth_header = base64.b64encode(
            '{0}:{1}'.format(self._client_id, self._client_secret).encode('ascii')
        )

        response = requests.post(
            url='https://accounts.spotify.com/api/token',
            headers={
                'Authorization': 'Basic {0}'.format(auth_header.decode('ascii'))
            },
            data={
                'grant_type': 'authorization_code',
                'code': authorization_code,
                'redirect_uri': self.redirect_uri,
                'scope': 'playlist-modify-public playlist-modify-private'
            }
        )

        return response.json()

    def _authorization_code_flow_authentication(self):
        url = 'https://accounts.spotify.com/authorize?{0}'.format(
            urlencode({
                'client_id': self._client_id,
                'response_type': 'code',
                'redirect_uri': self.redirect_uri,
                'scope': 'playlist-modify-public playlist-modify-private',
                'show_dialog': False
            })
        )

        return url

    def search_track(self, track_name, artist_name):
        """Search for a track using the Spotify Search API.

        Args:
            track_name (str): Track name
            artist_name (str): Artist name

        Returns:
            dict: Dict containing the song attributes
        """
        response = requests.get(
            'https://api.spotify.com/v1/search',
            params={
                'q': '{0} artist:{1}'.format(track_name, artist_name),
                'type': 'track',
                'limit': 1
            },
            headers={
                'Authorization': 'Bearer {0}'.format(self._access_token)
            }
        )
        response_json = response.json()

        track_attributes = {}  # init track_attributes as an empty dict

        if response.status_code != 200:
            logging.error(response_json["error"]["message"])
        elif response_json['tracks']['total'] == 0:
            logging.error("empty search")
        else:
            track = response_json['tracks']['items'][0]

            track_attributes = {
                'song_name': track['name'],
                'artist_name': track['artists'][0]['name'],
                'album_name': track['album']['name'],
                'popularity': track['popularity'],
                'duration_ms': track['duration_ms'],
                'explicit': track['explicit'],
                'spotify_uri': track['uri'],
                'album_image': track['album']['images'][0]['url']
            }

        return track_attributes

    def get_track_uris_from_playlist(self, limit=100):
        """Return the track URIs from the playlist

        Args:
            limit (int, optional): Maximum number of songs to return.\
                Defaults to 100.

        Returns:
            set: the songs URIs
        """
        response = requests.get(
            'https://api.spotify.com/v1/users/{0}/playlists/{1}/tracks'.format(
                self._user_id,
                self.playlist_id
            ),
            headers={'Authorization': 'Bearer {0}'.format(self._access_token)},
            params={
                'fields': ['items.track.uri'],
                'limit': limit
            }).json()

        track_uris = set([t['track']['uri'] for t in response['items']])

        return track_uris

    def add_tracks_to_playlist(self, track_uris, playlist_id):
        """Add spotify songs to playlist, using their URIs.

        Args:
            track_uris (list): List of songs URIs.

        Returns:
            json: Reponse from the Spotify API
        """
        response = requests.post(
            'https://api.spotify.com/v1/users/{0}/playlists/{1}/tracks'.format(
                self._user_id,
                playlist_id),
            headers={'Authorization': 'Bearer {0}'.format(self._access_token)},
            data=json.dumps({'uris': track_uris})
        )

        return response.json()
