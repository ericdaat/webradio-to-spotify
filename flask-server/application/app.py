from flask import Flask, jsonify, redirect, request, url_for
from spotify_api import SpotifyApi
from kshe_scraper import KSHEScraper
import logging
import uwsgi

app = Flask(__name__)
api = SpotifyApi()
scraper = KSHEScraper('http://player.listenlive.co/20101/en/songhistory')
playlist_uri = '3BCcE8T945z1MnfPWkFsfX'


# def update_playlist(signum):
#     logging.info('signum {0} received, will update playlist'.format(signum))
    
#     return redirect(url_for('update_playlist'))


# uwsgi.register_signal(99, "", update_playlist)
# uwsgi.add_timer(99, 60)


@app.route('/')
def index():
    return jsonify( _api_version='1.0')


@app.route('/scrap')
def scrap():
    song_history=scraper.get_song_history()

    return jsonify(song_history)


@app.route('/update_playlist', methods=['GET','POST'])
def update_playlist():
    song_history = scraper.get_song_history()
    spotify_songs = [api.search_track(s['title'], s['artist']) \
                        for s in song_history]

    spotify_songs = [s for s in spotify_songs if len(s) > 0]
    
    try:
        uris_in_playlist = api.get_track_uris_from_playlist(playlist_uri)
    except:
        uris_in_playlist = set()

    tracks_to_be_added = [s['spotify_uri'] for s in spotify_songs \
                            if s['spotify_uri'] not in uris_in_playlist]

    logging.info('will add {0} tracks'.format(len(tracks_to_be_added)))

    response = api.add_tracks_to_playlist(tracks_to_be_added, playlist_uri)

    return jsonify(**response)


@app.route('/auth')
def auth():
    return redirect(api._authorization_code_flow_authentication())


@app.route('/callback')
def callback():
    response = api._client_credentials_authentication(
            request.args['code'],
            api.redirect_uri)

    api._access_token = response["access_token"]
    token_type = response["token_type"]
    api._token_expires_in = response["expires_in"]

    logging.info('authenticated')

    return jsonify(
            authenticated=True,
            token_type=token_type,
            token_expires_in=api._token_expires_in
        )
