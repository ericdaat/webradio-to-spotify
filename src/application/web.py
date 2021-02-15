from flask import (
    Blueprint, render_template, current_app, redirect, url_for
)


bp = Blueprint("web", __name__, url_prefix="/web")


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/about')
def about():
    return render_template("about.html")


@bp.route('/auth')
def auth():
    return redirect(url_for("auth.auth"))


@bp.route('/sync')
def sync():
    # TODO: fix this hard coded playlist ID
    current_app.updater.sync_db_with_existing_songs("3BCcE8T945z1MnfPWkFsfX")

    return render_template(
        "index.html"
    )


@bp.route('/update')
def update():
    # TODO: use API instead
    inserted_songs, n_inserted_songs = current_app.updater.scrap_and_update()

    return render_template(
        "index.html",
        inserted_songs=inserted_songs if n_inserted_songs > 0 else None
    )
