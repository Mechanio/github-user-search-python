from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


# Stringfield for entering GitHub login
class SearchForm(FlaskForm):
    login = StringField('Enter GitHub login', validators=[InputRequired()])
