from flask import (
    Blueprint, redirect, current_app, request, url_for
)


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route('/', methods=['GET'])
def auth():
    url = current_app.updater.spotify_auth()

    return redirect(url)


@bp.route('/callback')
def callback():
    current_app.updater.spotify_callback(
        authorization_code=request.args["code"]
    )

    return redirect(url_for("web.index"))
