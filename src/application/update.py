from flask import Blueprint, jsonify, current_app


bp = Blueprint("update", __name__)


@bp.route('/')
def index():
    return jsonify(
        _api_version='1.1',
        spotify_authenticated=current_app.updater.is_authenticated
    )


@bp.route('/scrap', methods=['GET'])
def scrap():
    song_history = current_app.updater.get_radio_history()

    return jsonify(song_history)


@bp.route('/update_playlist', methods=['POST'])
def update_playlist():
    # get song history
    song_history = current_app.updater.get_radio_history()

    # spotify songs
    spotify_songs = current_app.updater.search_songs_in_spotify(song_history)

    # filter out already present songs and sync database
    spotify_filtered_songs = current_app.updater.filter_and_save_songs_to_db(
        spotify_songs
    )

    # upload the filtered out songs to the spotify playlist
    response = current_app.updater.add_songs_to_playlist(
        spotify_filtered_songs
    )

    return jsonify(**response)
