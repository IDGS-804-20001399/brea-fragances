from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flask_security import login_required, current_user, roles_required
from app.customer.forms import UserForm
from app.customer.models import Customer
from app.product.models import Product
from app import db
import json
from app.creditcard import luhn

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
    # cart = request.cookies.get('cartItems')
    # products = []
    # if cart is not None:
    #     cartItems = json.loads(cart)
    #     print(cartItems)
    #     for item in cartItems:
    #         products.append(Product.query.filter_by(id=item['item']).first())

    return render_template('cart.html', title='My cart', 
                           cart=cart,
                           subtotal=subtotal)

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
    if request.method == 'POST':
        card_number = request.form['card_number']
    
        if luhn.is_valid(card_number):
            flash("Card number is valid", 'success')
        else:
            flash("Card number is invalid", 'danger')
    return redirect(url_for('customer.cart'))

@customer.route('/statistics', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def statistics():
    return render_template('statistics.html', title='Statistics')