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

@order.route('/admin-order-details', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def adminOrderDetails():
    if request.method == 'POST':
        order = Order.query.filter_by(id=request.form.get("order_id")).first()
        customer = Customer.query.filter_by(id=order.user_id).first()
        orderDetails = OrderDetails.query.filter_by(order_id=request.form.get("order_id")).all()
    return render_template('adminOrderDetails.html', title='Order details',order=order, customer=customer, orderDetails=orderDetails)


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