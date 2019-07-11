import json
import base64
import logging
from urllib.parse import urlencode

import requests


class SpotifyApi(object):
    def __init__(self):
        with open(".spotify-token.json") as f:
            credentials = json.loads(f.read())

        self._user_id = credentials['user_id']
        self._client_id = credentials['client_id']
        self._client_secret = credentials['client_secret']
        self.redirect_uri = credentials['redirect_uri']
        self.playlist_id = credentials['playlist_id']

        # Will be set after spotify auth
        self._access_token = None
        self._refresh_token = None
        self._token_expires_in = None

    def _client_credentials_authentication(self, authorization_code=None):
        auth_header = base64.b64encode(
            '{0}:{1}'.format(self._client_id,
                             self._client_secret
                             ).encode('ascii'))

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
            })

        return response.json()

    def _authorization_code_flow_authentication(self):
        return 'https://accounts.spotify.com/authorize?{0}'.format(
            urlencode({
                'client_id': self._client_id,
                'response_type': 'code',
                'redirect_uri': self.redirect_uri,
                'scope': 'playlist-modify-public playlist-modify-private',
                'show_dialog': False
            }))

    def search_track(self, track_name, artist_name, limit=1):
        response = requests.get(
            'https://api.spotify.com/v1/search',
            params={
                'q': '{0} artist:{1}'.format(track_name, artist_name),
                'type': 'track',
                'limit': limit
            },
            headers={
                'Authorization': 'Bearer {0}'.format(self._access_token)
            }
        )
        response_json = response.json()

        if response.status_code != 200:
            logging.error(response_json["error"]["message"])
            return {}
        elif response_json['tracks']['total'] == 0:
            logging.error("empty search")
            return {}

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

    def get_track_uris_from_playlist(self):
        response = requests.get(
            'https://api.spotify.com/v1/users/{0}/playlists/{1}/tracks'.format(
                self._user_id,
                self.playlist_id
            ),
            headers={'Authorization': 'Bearer {0}'.format(self._access_token)},
            params={
                'fields': ['items.track.uri'],
                'limit': 100
            }).json()

        track_uris = set([t['track']['uri'] for t in response['items']])

        return track_uris

    def add_tracks_to_playlist(self, track_uris):
        return requests.post(
            'https://api.spotify.com/v1/users/{0}/playlists/{1}/tracks'.format(
                self._user_id,
                self.playlist_id),
            headers={'Authorization': 'Bearer {0}'.format(self._access_token)},
            data=json.dumps({'uris': track_uris})
        ).json()
