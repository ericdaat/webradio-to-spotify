import requests
import json
import base64
import pandas as pd
import datetime
import logging
from urllib  import urlencode


class SpotifyApi(object):
    def __init__(self):
        with open("../.spotify-token.json") as f:
            credentials = json.loads(f.read())

        self._user_id = credentials['user_id']
        self._client_id = credentials['client_id']
        self._client_secret = credentials['client_secret']
        self.redirect_uri = credentials['redirect_uri']
        self._access_token = None
        self._refresh_token = None
        self._token_expires_in = None


    def _client_credentials_authentication(self, authorization_code=None, redirect_uri=None):
        auth_header = base64.b64encode(
            '{0}:{1}'.format(self._client_id, self._client_secret)
        ).encode('ascii')

        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={'Authorization': 'Basic {0}'.format(auth_header.decode('ascii'))},
            data={
                'grant_type':'authorization_code',
                'code': authorization_code,
                'redirect_uri': redirect_uri,
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
        try:
            response = requests.get(
                'https://api.spotify.com/v1/search',
                params={
                    'q':'artist:"{0}"%20track:"{1}"'.format(artist_name, track_name),
                    'type':'track',
                    'limit': limit
                },
                headers={'Authorization': 'Bearer {0}'.format(self._access_token)}
            ).json()['tracks']['items'][0]
        except:
            logging.warning(
                'could not find track {0} from {1}'.format(
                    track_name, 
                    artist_name
                )
            )
            return {}

        return {
            'song_name': response['name'],
            'artist_name': response['artists'][0]['name'],
            'album_name': response['album']['name'],
            'popularity': response['popularity'],
            'duration_ms': response['duration_ms'],
            'explicit': response['explicit'],
            'spotify_uri': response['uri'],
            'album_image': response['album']['images'][0]['url']
        }


    def get_track_uris_from_playlist(self, playlist_uri):
        response = requests.get(
            'https://api.spotify.com/v1/users/{0}/playlists/{1}/tracks'.format(
                self._user_id,
                playlist_uri
            ),
            headers={'Authorization': 'Bearer {0}'.format(self._access_token)},
            params={
                'fields':['items.track.uri'],
                'limit': 100
            }).json()

        return set([t['track']['uri'] for t in response['items']])


    def add_tracks_to_playlist(self, track_uris, playlist_uri):
        return requests.post(
                'https://api.spotify.com/v1/users/{0}/playlists/{1}/tracks'.format(
                self._user_id,
                playlist_uri),
            headers={'Authorization': 'Bearer {0}'.format(self._access_token)},
            data=json.dumps({'uris': track_uris})
        ).json()