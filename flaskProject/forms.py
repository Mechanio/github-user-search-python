from flask_wtf import FlaskForm
from wtforms import StringField


# Stringfield for entering GitHub login
class SearchForm(FlaskForm):
    login = StringField('Enter GitHub login')
