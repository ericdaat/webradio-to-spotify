import os
import logging

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from src.playlist_updater import Updater


def create_app():
    """ Flask app factory that creates and configure the app.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.logger.setLevel(logging.DEBUG)

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
    from src.application import api, auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)

    return app
