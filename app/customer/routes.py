from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flask_security import login_required, current_user, roles_required
from app.customer.forms import UserForm
from app.customer.models import Customer
from app.product.models import Product, ProductInventory
from app.order.models import Order, OrderDetails
from app import db
import json
from app.creditcard import luhn
from datetime import date

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
    return render_template('myOrders.html', title='My Orders')

@customer.route('/cart', methods=["POST", "GET"])
@login_required
@roles_required('customer')
def cart():
    cart = session.get('cart')
    if not cart:
        cart = []
    subtotal = sum([i['product']['price'] * i['quantity'] for i in cart])
    delivery_fee = 99 if subtotal < 1000 else 0
    total = subtotal + delivery_fee
    if request.method == 'POST':
        card_number = request.form['card_number']
        if luhn.is_valid(card_number):
            order = Order(
                payment = f'Card {card_number}',
                delivery_method = 'Shipping',
                delivery_fee = delivery_fee,
                status = 'Ordered',
                user_id = current_user.id,
            )
            db.session.add(order)
            db.session.commit()
            for product in cart:
                product_id = product['product']['id']
                quantity = product['quantity']
                detail = OrderDetails(
                    order_id = order.id,
                    product_id = product_id,
                    quantity = quantity,
                    price = product['product']['price'],
                )
                db.session.add(detail)
                db.session.commit()
                p = Product.query.get(product_id)
                make = p.makes.filter(ProductInventory.expiration_date > date.today()).order_by(ProductInventory.expiration_date).first()
                make.available_quantity -= quantity
                db.session.commit()
                cart = []
                flash("Order made successfully", 'success')
        else:
            flash("Card number is invalid", 'danger')
    return render_template('cart.html', title='My cart', 
                           cart=cart,
                           subtotal=subtotal,
                           delivery_fee=delivery_fee,
                           total = total)

@customer.route('/checkout', methods=["POST", "GET"])
@login_required
@roles_required('customer')
def checkout():
    cart = request.cookies.get('cartItems')
    if cart is not None:
        cartItems = json.loads(cart)
        print(cartItems)
    return render_template('cart.html', title='My cart', products=products)

@customer.route('/order-details', methods=["POST", "GET"])
@login_required
@roles_required('customer')
def details():
    return render_template('orderDetails.html', title='Order Details')

@customer.route('/validateCard', methods=["POST", "GET"])
@login_required
@roles_required('customer')
def validate():
    return redirect(url_for('customer.cart'))

@customer.route('/statistics', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def statistics():
    return render_template('statistics.html', title='Statistics')