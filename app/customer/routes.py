from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_security import login_required, current_user, roles_required
from app.forms import UserForm

customer = Blueprint('customer', __name__,
                 template_folder='templates',
                 url_prefix='/customer')
            
@customer.route('/my-info', methods=["POST", "GET"])
# @login_required
# @roles_required('customer')
def index():
    form=UserForm(request.form)

    if request.method == "POST":
        return redirect(url_for("customer.index"))
    
    return render_template('customer.html', title='My Information', form=form)

@customer.route('/my-orders', methods=["POST", "GET"])
# @login_required
# @roles_required('customer')
def orders():
    return render_template('orders.html', title='My Orders')

@customer.route('/order-details', methods=["POST", "GET"])
# @login_required
# @roles_required('customer')
def details():
    return render_template('details.html', title='Order Details')
