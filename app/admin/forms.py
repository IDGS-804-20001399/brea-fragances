from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

class ProductForm(FlaskForm):
    name=StringField('Name', [DataRequired(message='Must not be empty')])
    price=FloatField('Price', [NumberRange(min=0.1, message='The value must be greater than 0.1')])
    stock=IntegerField('Stock', [NumberRange(min=1, message='The value must be greater than 1')])
    image=StringField('Image', [DataRequired(message='Must not be empty')])
    submit = SubmitField('Add product')