from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app import user_datastore

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    names=StringField('Names', [DataRequired(message='Must not be empty')])
    lastnames=StringField('Last names', [DataRequired(message='Must not be empty')])
    address=StringField('Address', [DataRequired(message='Must not be empty')])
    phone=StringField('Phone Number', [Length(min=10, max=10, message='Must not be empty')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if user_datastore.get_user(email):
            raise ValidationError('That email is taken. Please choose a different one.')
