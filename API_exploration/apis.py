"""apis.py"""
from datetime import datetime

from flask import (current_app as app,
                   Blueprint,
                   redirect,
                   request,
                   render_template,
                   url_for,
                   )
from flask_wtf.csrf import CSRFError

from API_exploration.API import (xkcd as xkcd_api,  # Alias to avoid name clash with route.
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
def xkcd():
    """
    xkcd

    By default return latest xkcd comic.

    select_comic_number dropdown options have to be prepared and attached to
    form before validation, or validation for that field will fail, even if it
    was not submitted.
    select_comic_number must be evaluated last, as it submits a value (initial
    value 1) when the form is submitted, so it needs to be evaluated only
    if none of the other buttons was pressed.

    TODO Return desired comic number/date via form.
    ? allow search by date? have to build up db of dates
    ? this would not be too hard as json for comics has the dates as mm dd yyyy
    ? keeping db updated would be a chron job?

    """
    requested_comic_number = None  # Default, will return latest.
    current_date = datetime.now()

    form = xkcd_api.xkcdForm()

    if request.method == 'POST':
        form.select_comic_number.choices = [  # Prep valid choices to validate dropdown options.
            num for num in range(1, int(form.latest_comic_number.data) + 1)]
        if form.validate_on_submit():
            if form.first.data:
                requested_comic_number = 1
            elif form.previous.data:
                requested_comic_number = int(form.current_comic.data) - 1
            elif form.next.data:
                requested_comic_number = int(form.current_comic.data) + 1
            elif form.latest.data:
                requested_comic_number = None
            elif form.select_comic_number:
                requested_comic_number = form.select_comic_number.data

    comic_data = xkcd_api.get_comic_data(comic_number=requested_comic_number,
                                         cache_hour=(current_date.date, current_date.hour))
    # Prepare form:
    comic_choices = [num for num in range(1, comic_data['latest_comic_number'] + 1)]
    comic_choices.remove(404)  # Remove nonexistent comic
    form.select_comic_number.choices = comic_choices
    form.select_comic_number.choices.remove(comic_data['comic_number'])  # Remove current comic

    form.current_comic.data = comic_data['comic_number']  # Set current comic
    form.latest_comic_number.data = comic_data['latest_comic_number']  # Set latest comic

    return render_template('APIs/xkcd.html',
                           comic_number=comic_data['comic_number'],
                           comic_url=comic_data['comic_url'],
                           comic_image_url=comic_data['comic_image_url'],
                           comic_title=comic_data['comic_title'],
                           comic_alt_text=comic_data['comic_alt_text'],
                           latest_comic_number=comic_data['latest_comic_number'],
                           form=form)


@bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    """
    Redirects user to requested page in event of CSRF Error.

    Assumes all routes are under my_site blueprint.
    Assumes all route functions have same name as their url.
    """
    return redirect(url_for(f'apis.{request.path[1:-1]}'))


if __name__ == '__main__':
    app.run()
