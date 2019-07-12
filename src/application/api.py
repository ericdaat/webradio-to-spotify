from flask import Blueprint, jsonify, current_app


bp = Blueprint("api", __name__)


@bp.route('/api')
def index():
    return jsonify(
        _api_version='1.1',
        spotify_authenticated=current_app.updater.is_authenticated
    )


@bp.route('/api/update_playlist', methods=['POST'])
def update_playlist():
    inserted_songs = current_app.updater.scrap_and_update()

    return jsonify(
        updated=True,
        inserted_songs=inserted_songs
    )
