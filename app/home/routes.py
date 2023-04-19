from flask import render_template, url_for, flash, redirect, request, Blueprint, session
from flask_security import login_required, current_user, roles_required, roles_accepted
from app.product.models import Product
import json

home = Blueprint('home', __name__,
                 template_folder='templates')
            
@home.route('/')
def index():
    products = Product.query.all()
    return render_template('home.html', title='Brea Fragances - Home', products=products)

@home.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('allProducts.html', title='Products', products=products)

@home.route('/add/<int:product_id>', methods=['POST'])
@login_required
@roles_accepted('customer')
def add(product_id):
    cart = session.get('cart')
    product = Product.query.get(product_id).__dict__
    if not cart:
        cart = []
        cart.append({'product': product, 'quantity': 1})
    else:
        result = next((item for item in cart if item["product"]['id'] == product_id), False)
        if result:
            result['quantity'] += 1
        else:
            cart.append({'product': product, 'quantity': 1})
    session['cart'] = cart
    flash('Producto agregado al carrito', 'success')
    return redirect(request.form.get("url"))


@home.route('/edit-quantity/<int:product_id>', methods=['POST'])
@login_required
@roles_accepted('customer')
def edit_quantity(product_id):
    cart = session.get('cart')
    if cart:
        result = next((item for item in cart if item["product"]['id'] == product_id), False)
        if result:
            result['quantity'] = int(request.form.get("quantity"))
    return redirect(url_for('customer.cart'))


@home.route('/remove/<int:product_id>', methods=['GET'])
@login_required
@roles_accepted('customer')
def remove(product_id):
    cart = session.get('cart')
    if cart:
        result = next((item for item in cart if item["product"]['id'] == product_id), False)
        if result:
            cart.remove(result)
    return redirect(url_for('customer.cart'))


