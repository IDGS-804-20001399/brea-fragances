from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_security import login_required, current_user, roles_required
from app.order.models import Order, OrderDetails
from app.product.models import Product
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
def ordersOrders():
    orderDetails = OrderDetails.query.filter(order_id="1").all()
    return render_template('ordersDetails.html', title='Order details')

@order.route('/customers', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def customers():
    return render_template('customers.html', title='Customers list')
