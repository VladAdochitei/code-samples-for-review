from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User

class LoginForm(FlaskForm):
    email       = StringField("Email", validators=[DataRequired(), Email()])
    password    = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    remember_me = BooleanField("Remember Me")
    submit      = SubmitField("Login")  

class RegisterForm(FlaskForm):
    email            = StringField("Email", validators=[DataRequired(), Email()])
    password         = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=16)])
    password_confirm = PasswordField("Confirm password", validators=[DataRequired(), Length(min=6, max=16), EqualTo('password')])
    first_name       = StringField("First name", validators=[DataRequired(), Length(min=2, max=56)])
    last_name        = StringField("Last name", validators=[DataRequired(), Length(min=2, max=56)])
    submit           = SubmitField("Register")  

    # Make sure validate_<name> has the same name with the field that you want to validate
    def validate_email(self, email):
        user = User.objects(email = email.data).first()
        if user:
            raise ValidationError("Email is already in use. Please use another email.")