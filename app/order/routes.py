from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_security import login_required, current_user, roles_required, roles_accepted
from app.order.models import Order, OrderDetails
from app.product.models import Product
from app.customer.models import Customer
from app import db

order = Blueprint('order', __name__,
                 template_folder='templates',
                 url_prefix='/order')
            
@order.route('/orders', methods=["POST", "GET"])
@login_required
@roles_accepted('admin', 'seller')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', title='Orders', orders=orders)

@order.route('/admin-order-details/<int:order_id>', methods=["GET"])
@login_required
@roles_accepted('admin', 'seller', 'customer')
def adminOrderDetails(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('adminOrderDetails.html', title='Order details',order=order)


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
    order = Order.query.filter_by(user_id=customer_id).first()
    return render_template('ordersDetails.html', title='Order details', order=order)