from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_security import login_required, current_user, roles_required
from app.order.models import Order, OrderDetails
from app.product.models import Product
from app.customer.models import Customer
from app import db

order = Blueprint('order', __name__,
                 template_folder='templates',
                 url_prefix='/order')
            
@order.route('/orders', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', title='Orders', orders=orders)

@order.route('/order-details', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def ordersDetails():
    orderDetails = OrderDetails.query.filter(order_id=request.form.get('id')).all()
    return render_template('ordersDetails.html', title='Order details')

@order.route('/customers', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', title='Customers list', customers = customers)

@order.route('/customer-details/<int:customer_id>', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def customerDetails(customer_id):
    # NECESITO DATOS DE LA ORDER Y LOS PRODUCTOS DE LA MISMA
    orderDetails = OrderDetails.query.filter(order_id=customer_id).all()
    return render_template('ordersDetails.html', title='Order details', orderDetails=orderDetails)