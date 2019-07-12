from flask import Blueprint, render_template


bp = Blueprint("web", __name__, url_prefix="/web")


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/auth')
def auth():
    return render_template("index.html")


@bp.route('/update')
def update():
    return render_template("index.html")
