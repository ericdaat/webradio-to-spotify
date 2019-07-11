import logging

from flask import Blueprint, jsonify, current_app


bp = Blueprint("updater", __name__)


@bp.route('/')
def index():
    return jsonify(
        _api_version='1.0',
        _spotify_token=current_app.spotify._access_token is not None
    )


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
