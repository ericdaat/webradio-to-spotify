from flask import Blueprint, redirect, jsonify, current_app, request


bp = Blueprint("auth", __name__)


@bp.route('/auth', methods=['GET'])
def auth():
    url = current_app.updater.spotify_auth()

    return redirect(url)


@bp.route('/callback')
def callback():
    current_app.updater.spotify_callback(
        authorization_code=request.args["code"]
    )

    return jsonify(
        authenticated=True
    )
