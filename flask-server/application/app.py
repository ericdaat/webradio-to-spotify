from flask import Flask, jsonify, redirect, request
from spotify_api import SpotifyApi
from kshe_scraper import KSHEScraper

app = Flask(__name__)
api = SpotifyApi()
scraper = KSHEScraper('http://player.listenlive.co/20101/en/songhistory')

@app.route('/')
def index():
    return jsonify( _api_version='1.0')


@app.route('/scrap')
def scrap():
    song_history=scraper.get_song_history()
    return jsonify(song_history)


@app.route('/update_playlist', methods=['GET','POST'])
def update_playlist():
    playlist_uri = '3BCcE8T945z1MnfPWkFsfX'
    song_history = scraper.get_song_history()
    spotify_songs = [api.search_track(s['title'], s['artist']) \
                        for s in song_history]

    response = api.add_tracks_to_playlist(
            [s['spotify_uri'] for s in spotify_songs if len(s)>0],
            playlist_uri)

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

    return jsonify(
            authenticated=True,
            token_type=token_type,
            token_expires_in=api._token_expires_in
            )
