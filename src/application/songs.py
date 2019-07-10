import logging

from flask import Blueprint, redirect, jsonify, current_app, request


bp = Blueprint("songs", __name__)


@bp.route('/')
def index():
    return jsonify(_api_version='1.0')


@bp.route('/scrap', methods=['GET'])
def scrap():
    song_history = current_app.scraper.get_song_history()

    return jsonify(song_history)


@bp.route('/update_playlist', methods=['POST'])
def update_playlist():
    song_history = current_app.scraper.get_song_history()
    spotify_songs = [current_app.spotify.search_track(s['title'], s['artist'])
                     for s in song_history]

    spotify_songs = [s for s in spotify_songs if len(s) > 0]

    try:
        uris_in_playlist = current_app.spotify.get_track_uris_from_playlist()
    except:
        uris_in_playlist = set()

    tracks_to_be_added = [s['spotify_uri'] for s in spotify_songs
                          if s['spotify_uri'] not in uris_in_playlist]

    logging.info('will add {0} tracks'.format(len(tracks_to_be_added)))

    response = current_app.spotify.add_tracks_to_playlist(tracks_to_be_added)

    return jsonify(**response)


@bp.route('/auth', methods=['GET'])
def auth():
    return redirect(
        current_app.spotify._authorization_code_flow_authentication()
    )


@bp.route('/callback')
def callback():
    response = current_app.spotify._client_credentials_authentication(
        request.args['code']
    )

    current_app.spotify._access_token = response['access_token']
    token_type = response['token_type']
    current_app.spotify._token_expires_in = response['expires_in']

    logging.info('authenticated')

    return jsonify(
        authenticated=True,
        token_type=token_type,
        token_expires_in=current_app.spotify._token_expires_in
    )
