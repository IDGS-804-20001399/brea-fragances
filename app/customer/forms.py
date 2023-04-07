from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app import user_datastore
from flask_security import current_user
from app.auth.models import User

class UserForm(FlaskForm):
    names=StringField('Names', [DataRequired(message='Must not be empty')])
    lastnames=StringField('Last names', [DataRequired(message='Must not be empty')])
    address=StringField('Address', [DataRequired(message='Must not be empty')])
    phone=StringField('Phone', [Length(min=10, max=10, message='Must not be empty')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Edit profile')

    def validate_email(self, email):
        if email.data != current_user.email:
            if user_datastore.get_user(email):
                raise ValidationError('That email is taken. Please choose a different one.')
