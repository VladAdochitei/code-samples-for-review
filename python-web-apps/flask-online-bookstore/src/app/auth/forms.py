from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError 
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from app.models import User

class LoginForm(FlaskForm):
    '''
    Form to login an user
    '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
    '''
    Form to register a new user
    '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message="Passwords must match!")])
    password_confirm = PasswordField('Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match!")])
    submit = SubmitField('Register')

    def validate_email(self, field):
        # Function to check if the e-mailis already in the database
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")
        
    def validate_username(self, field):
        # Function to check if the username is already in the database
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Your username has been registered already!")
        