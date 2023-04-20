from flask import render_template, url_for, flash, redirect, request, Blueprint, session, current_app
from flask_security import login_required, current_user, roles_required
from app.customer.forms import UserForm, StatsForm
from app.customer.models import Customer
from app.product.models import Product, ProductInventory
from app.order.models import Order, OrderDetails
from app.supply.models import SupplyBuys, Supply
from app import db
import json
from app.creditcard import luhn
from datetime import date, datetime, timedelta

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
    orders = Order.query.filter_by(user_id = current_user.id).all()
    return render_template('orders.html', title='My Orders', orders=orders)

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
                p = Product.query.get(product_id)
                if p.stock < quantity:
                    for detail in order.details:
                        db.session.delete(detail)
                        db.session.commit()
                    db.session.delete(order)
                    db.session.commit()
                    flash('Not enough stock to process your order :(', 'danger')
                    return redirect(url_for('customer.cart'))
                detail = OrderDetails(
                    order_id = order.id,
                    product_id = product_id,
                    quantity = quantity,
                    price = product['product']['price'],
                )
                db.session.add(detail)
                db.session.commit()
                #discounting from inventory
                makes = p.makes.filter(ProductInventory.expiration_date > date.today()).order_by(ProductInventory.expiration_date).all()
                index = 0
                remaining = quantity
                while True:
                    make = makes[index]
                    difference = make.available_quantity - remaining 
                    if difference >= 0:
                        make.available_quantity = difference
                        db.session.commit()
                        break
                    remaining = abs(difference)
                    difference = 0
                    make.available_quantity = 0
                    db.session.commit()
                    index += 1



                cart = []
                current_app.logger.critical(f"USER {current_user.email} MADE A BUY")
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
    end_date = date.today()
    start_date = date.today() - timedelta(days=30)
    form = StatsForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
    elif request.method == 'POST':
        form.end_date.data = end_date
        form.start_date.data = start_date
    expenses = SupplyBuys.query.filter(SupplyBuys.buy_date >= start_date).filter(SupplyBuys.buy_date <= end_date).order_by(SupplyBuys.buy_date.desc()).all()
    incomes = Order.query.filter(Order.date >= start_date).filter(Order.date <= end_date).order_by(Order.date.desc()).all()
    total_expenses = sum([i.total_cost for i in expenses])
    total_income = sum([i.subtotal for i in incomes])
    earnings = total_income - total_expenses
    return render_template('statistics.html', 
                           title='Statistics',
                           expenses = expenses,
                           incomes = incomes,
                           total_expenses = total_expenses,
                           total_income = total_income,
                           earnings = earnings,
                           form = form
                           )