import os
import logging

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from src.spotify import SpotifyApi
from src.scraping import KSHEScraper


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
    app.spotify = SpotifyApi()
    app.scraper = KSHEScraper()

    # blueprints
    from application import home
    app.register_blueprint(home.bp)

    return app
