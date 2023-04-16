from flask_wtf import FlaskForm
from wtforms.fields import (StringField, SubmitField, FloatField, DateField,
                            IntegerField)
from wtforms.validators import DataRequired, NumberRange 
from flask_wtf.file import FileField, FileAllowed
from app import supply_pics

class SupplyForm(FlaskForm):
    name=StringField('Name', [DataRequired(message='Must not be empty')])
    cost=FloatField('Cost', [NumberRange(min=0.1, message='The value must be greater than 0.1')])
    buy_unit=StringField('Buy unit', [DataRequired(message='Must not be empty')])
    use_unit=StringField('Use unit', [DataRequired(message='Must not be empty')])
    equivalence=FloatField('Equivalence', [NumberRange(min=0.1, message='The value must be greater than 0.1')])
    image=FileField(validators=[FileAllowed(supply_pics, 'Image only')])
    submit = SubmitField('Save supply')

class BuySupplyForm(FlaskForm):
    expiration_date = DateField('Expiration date', [DataRequired('Must not be empty')])
    quantity = IntegerField('Quantity', [DataRequired('Must not be empty'),
                                         NumberRange(min=1, message='The value must be greater than 1.')])
