from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed
from app import supply_pics

class SupplierForm(FlaskForm):
    name=StringField('Name', [DataRequired(message='Must not be empty')])
    contact=StringField('Contact Info (Email/Phone)', [DataRequired(message='Must not be empty')])
    product=StringField('Product', [DataRequired(message='Must not be empty')])
    submit = SubmitField('Save supplier')