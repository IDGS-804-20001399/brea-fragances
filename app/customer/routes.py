from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_security import login_required, current_user, roles_required
from app.customer.forms import UserForm
from app.customer.models import Customer
from app import db

customer = Blueprint('customer', __name__,
                 template_folder='templates',
                 url_prefix='/customer')
            
@customer.route('/my-info', methods=["POST", "GET"])
@login_required
@roles_required('customer')
def index():
    form=UserForm()
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        customer.names = form.names.data
        customer.lastnames = form.lastnames.data
        customer.address = form.address.data
        customer.phone = form.phone.data
        customer.user.email = form.email.data
        db.session.commit()
        flash('Information updated successfully', 'success')
        return redirect(url_for('customer.index'))
    elif request.method == 'GET':
        form.names.data = customer.names
        form.lastnames.data = customer.lastnames
        form.address.data = customer.address
        form.phone.data = customer.phone
        form.email.data = customer.user.email
    return render_template('customer.html', title='My Information', form=form)

@customer.route('/my-orders', methods=["POST", "GET"])
@login_required
@roles_required('customer')
def myOrders():
    return render_template('orders.html', title='My Orders')

@customer.route('/order-details', methods=["POST", "GET"])
@login_required
@roles_required('customer')
def details():
    return render_template('details.html', title='Order Details')

@customer.route('/customers', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def customers():
    return render_template('customers.html', title='Customers list')

@customer.route('/customers-orders', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def customersOrders():
    return render_template('customersOrders.html', title='Customers orders')

@customer.route('/statistics', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def statistics():
    return render_template('statistics.html', title='Statistics')