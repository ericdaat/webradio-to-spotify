from flask import Blueprint, jsonify, current_app


bp = Blueprint("update", __name__)


@bp.route('/')
def index():
    return jsonify(
        _api_version='1.1',
        spotify_authenticated=current_app.updater.is_authenticated
    )


@bp.route('/update_playlist', methods=['POST'])
def update_playlist():
    current_app.updater.scrap_and_update()

    return jsonify(updated=True)
