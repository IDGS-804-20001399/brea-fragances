from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_security import login_required, current_user, roles_required

home = Blueprint('home', __name__,
                 template_folder='templates',
                 url_prefix='/home')
            
@home.route('/')
def index():
    return render_template('home.html', title='Brea Fragances - Home')