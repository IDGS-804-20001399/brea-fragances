from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app import user_datastore
from flask_security import current_user
from app.order.models import Order

class OrderForm(FlaskForm):
    total=FloatField('Total', [DataRequired(message='Must not be empty')])
    payment=StringField('payment Method', [DataRequired(message='Must not be empty')])
    status=StringField('Status', [DataRequired(message='Must not be empty')])
    submit = SubmitField('Edit profile')