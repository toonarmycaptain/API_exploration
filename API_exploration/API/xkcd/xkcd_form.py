""" Form for xkcd comic navigation """

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import (IntegerField,
                     SelectField,
                     SubmitField,
                     HiddenField,
                     )
from wtforms.validators import DataRequired


class xkcdForm(FlaskForm):
    first = SubmitField('First')
    previous = SubmitField('Previous')
    select_comic_number = SelectField('comic_number', choices=[], coerce=int, validators=[DataRequired()])
    comic_number_selected = SubmitField('Select')
    next = SubmitField('Next')
    latest = SubmitField('Latest')
    current_comic = HiddenField(label='current_comic_number')
    latest_comic_number = HiddenField('latest_comic_number')
