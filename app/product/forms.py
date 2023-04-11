from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed
from app import product_pics

class ProductForm(FlaskForm):
    name=StringField('Name', [DataRequired(message='Must not be empty')])
    description=StringField('Description', [DataRequired(message='Must not be empty')])
    price=FloatField('Price', [NumberRange(min=0.1, message='The value must be greater than 0.1')])
    image=FileField(validators=[FileAllowed(product_pics, 'Image only')])
    submit = SubmitField('Save product')