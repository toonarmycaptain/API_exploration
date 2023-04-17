""" App factory """
import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

ABOUT_TEXT_STRING = (
    b'<html>'
    b'<p>I am <span style="font-family:monospace;">toonarmycaptain</span>, this is a demonstration '
    b'website showcasing various APIs I enjoy.</p>'
    b'<p>The repo for the site is '
    b'<a href="https://github.com/toonarmycaptain/API_exploration/">'
    b'API_exploration</a>.</p>'
    b'<p>I primarily created the site using Flask, some basic CSS, and pytest.</p>'
    b'<p>Any comments or enquiries can be directed to my '
    b'<a href="https://toonarmycaptain.pythonanywhere.com/contact/">contact page</a>, or '
    b'<a href="https://twitter.com/toonarmycaptain">toonarmycaptain</a>.</p>'
    b'</html>')


def create_app(test_config: dict|None = None) -> Flask:
    """
    Create application instance.

    :param test_config: dict or None
    :return: Flask
    """
    app: Flask = Flask(__name__)
    # Defaults to be overridden by instance config:

    app.config.from_pyfile('default_config.py')
    SECRET_KEY = os.urandom(512)
    app.config.update(SECRET_KEY=SECRET_KEY)

    # Load runtime config:
    if test_config is None:  # Load production config.
        app.config.from_pyfile('app_config.py')
    else:  # Load testing config:
        app.config.update(test_config)



    # Setup CSRF
    CSRF_SECRET_KEY = os.urandom(512)
    app.config.update(WTF_CSRF_SECRET_KEY=CSRF_SECRET_KEY)

    csrf = CSRFProtect(app)

    from API_exploration import apis
    app.register_blueprint(apis.bp)

    @app.route('/about_text/')
    def about_text() -> bytes:
        """
        Basic about text, mainly used for testing.

        :return: bytes
        """
        return ABOUT_TEXT_STRING

    return app
