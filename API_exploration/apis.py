"""apis.py"""
from flask import (current_app as app,
                   Blueprint,
                   redirect,
                   request,
                   render_template,
                   url_for,
                   )
from flask_wtf.csrf import CSRFError

from API_exploration.API import (xkcd,
                                 )

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


@bp.route('/xkcd/', methods=['GET', 'POST'])
def xkcd_comic():  # Function named to avoid name clash with API import.
    """
    xkcd

    By default return latest xkcd comic.

    TODO Return chosen comic number via form.
    ? allow search by date? have to build up db of dates
    ? this would not be too hard as json for comics has the dates as mm dd yyyy
    ? keeping db updated would be a chron job?

    """
    requested_comic = None  # Default, will return latest.
    if request.method == 'POST':
        requested_comic = request.form['requested_comic']

    comic_data = xkcd.get_comic_data(requested_comic)

    return render_template('APIs/xkcd.html',
                           comic_number=comic_data['comic_number'],
                           comic_url=comic_data['comic_url'],
                           comic_image_url=comic_data['comic_image_url'],
                           comic_title=comic_data['comic_title'],
                           comic_alt_text=comic_data['comic_alt_text'],
                           latest_comic_number=comic_data['latest_comic_number'],
                           )


@bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    """
    Redirects user to requested page in event of CSRF Error.

    Assumes all routes are under my_site blueprint.
    """
    return redirect(url_for(f'apis.{request.path[1:-1]}'))


if __name__ == '__main__':
    app.run()
