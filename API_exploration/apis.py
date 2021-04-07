"""apis.py"""
from flask import (current_app as app,
                   Blueprint,
                   redirect,
                   request,
                   render_template,
                   url_for,
                   )
from flask_wtf.csrf import CSRFError

bp = Blueprint("apis", __name__)


@bp.route('/favicon.ico', methods=['GET'])
def favicon():
    """
    Serve webpage icon.
    """
    return redirect(url_for('static',
                            filename='favicon.ico',
                            mimetype='image/vnd.microsoft.icon'
                            )
                    )


@bp.route('/', methods=['GET'])
def base_url():
    """Redirect bare url to home page."""
    return redirect(url_for('apis.home'), code=301)


@bp.route('/home/', methods=['GET'])
def home():
    """Home page."""
    return render_template('home.html')




@bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    """
    Redirects user to requested page in event of CSRF Error.

    Assumes all routes are under my_site blueprint.
    """
    return redirect(url_for(f'apis.{request.path[1:-1]}'))


if __name__ == '__main__':
    app.run()
