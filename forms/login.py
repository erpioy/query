from flask_wtf import FlaskForm
from wtforms import StringField,ValidationError
from wtforms.validators import Email,EqualTo,Length
from models.user import UserModel

class LoginForm(FlaskForm):
    pass