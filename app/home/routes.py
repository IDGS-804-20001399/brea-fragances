from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_security import login_required, current_user, roles_required, roles_accepted
from app.product.models import Product
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