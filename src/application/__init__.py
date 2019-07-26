import os
import logging

from flask import Flask, redirect, url_for
from werkzeug.contrib.fixers import ProxyFix

from src.playlist_updater import Updater


def create_app():
    """ Flask app factory that creates and configure the app.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.logger.setLevel(logging.INFO)

    # instance dir
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # objects
    app.updater = Updater()

    # blueprints
    from src.application import api, auth, web
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(web.bp)

    # default route
    @app.route("/")
    def index():
        return redirect(url_for("web.index"))

    return app
