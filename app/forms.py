from wtforms import Form, StringField, IntegerField, EmailField, validators, RadioField, FloatField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app import user_datastore

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    style1={'placeholder': 'Confirm Password'}
    style2={'placeholder': 'Names'}
    style3={'placeholder': 'Password'}
    style4={'placeholder': 'Email'}
    style5={'placeholder': 'Last Names'}
    style6={'placeholder': 'Address'}
    style7={'placeholder': 'Phone Number'}
    names=StringField('', [validators.DataRequired(message='Must not be empty')], render_kw=style2)
    lastnames=StringField('', [validators.DataRequired(message='Must not be empty')], render_kw=style5)
    address=StringField('', [validators.DataRequired(message='Must not be empty')], render_kw=style6)
    phone=IntegerField('', [validators.number_range(min=10, max=10, message='Must not be empty')], render_kw=style7)
    email = StringField('',
                        validators=[DataRequired(), Email()], render_kw=style4)
    password = PasswordField('', validators=[DataRequired()], render_kw=style3)
    confirm_password = PasswordField('',
                                     validators=[DataRequired(), EqualTo('password')], render_kw=style1)
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if user_datastore.get_user(email):
            raise ValidationError('That email is taken. Please choose a different one.')

class UserForm(Form):
    style2={'placeholder': 'Names'}
    style4={'placeholder': 'Email'}
    style3={'placeholder': 'Password'}
    style5={'placeholder': 'Last Names'}
    style6={'placeholder': 'Address'}
    style7={'placeholder': 'Phone Number'}
    style1={'placeholder': 'Id', 'type': 'hidden'}
    id=IntegerField('', [validators.number_range(min=1, max=20, message='Must not be empty')], render_kw=style1)
    names=StringField('', [validators.DataRequired(message='Must not be empty')], render_kw=style2)
    lastnames=StringField('', [validators.DataRequired(message='Must not be empty')], render_kw=style5)
    address=StringField('', [validators.DataRequired(message='Must not be empty')], render_kw=style6)
    phone=IntegerField('', [validators.number_range(min=10, max=10, message='Must not be empty')], render_kw=style7)
    password=StringField('', [validators.DataRequired(message='Must not be empty')], render_kw=style3)
    email=EmailField('', [validators.DataRequired(message='Must not be empty'), validators.Email(message='Ingresa un correo valido')], render_kw=style4)

class ProductForm(Form):
    style1={ 'placeholder': 'Name'}
    style2={ 'placeholder': 'Price'}
    style3={ 'placeholder': 'Stock'}
    style4={ 'placeholder': 'Image'}
    name=StringField('', [validators.DataRequired(message='Must not be empty')], render_kw=style1)
    price=FloatField('', [validators.number_range(min=0, message='Must not be empty')], render_kw=style2)
    stock=IntegerField('', [validators.number_range(min=0, message='Must not be empty')], render_kw=style3)
    image=StringField('', [validators.DataRequired(message='Must not be empty')], render_kw=style4)