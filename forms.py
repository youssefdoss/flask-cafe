"""Forms for Flask Cafe."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, URL, Email, Length
import email_validator

class AddEditCafeForm(FlaskForm):
    '''Form for adding/editing cafes'''

    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    url = StringField('URL', validators=[Optional(), URL()])
    address = TextAreaField('Address', validators=[InputRequired()])
    city_code = SelectField('City')
    image_url = StringField('Image', validators=[Optional(), URL()])

class SignupForm(FlaskForm):
    """Form for signing up users."""

    username = StringField('Username', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('First Name', validators=[InputRequired()])
    description = TextAreaField('Description')
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('Image URL', validators=[Optional(), URL()])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])