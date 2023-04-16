from flask import render_template, url_for, flash, redirect, request, Blueprint, make_response
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
@roles_accepted('customer', 'admin')
def products():
    products = Product.query.all()
    return render_template('allProducts.html', title='Products', products=products)

@home.route('/add', methods=['POST', 'GET'])
@login_required
@roles_accepted('customer', 'admin')
def add():
    products = Product.query.all()
    resp = make_response(render_template('allProducts.html', title='Products', products=products))
    product_id = int(request.form.get("product_id"))
    if request.method == "POST":
        product_id = int(request.form.get("product_id"))
        cart = request.cookies.get('cartItems')
        if cart is not None:
            cartItems = json.loads(cart)
            if any(item["item"] == product_id for item in cartItems):
                flash('The item is already in the cart', 'danger')
                return resp
            else:
                cartItems.append({"item": product_id})
                resp.set_cookie('cartItems', json.dumps(cartItems))
                flash('Item added to cart successfully', 'success')
                return resp
        else:
            cartItems = [{"item": product_id}]
            resp.set_cookie('cartItems', json.dumps(cartItems))
            flash('Item added to cart successfully', 'success')
            return resp

    return resp

