from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.forms import LoginForm, RegistrationForm
from app.auth.models import User
from flask_security.utils import encrypt_password, verify_password, login_user, logout_user
from flask_security import login_required 

auth = Blueprint('auth', __name__,
                 template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def loginFunc():
    form = LoginForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if verify_password(form.password.data, user.password):
                login_user(user, form.remember.data)
                if user.has_role('admin'):
                    index = 'admin.index'
                else:
                    index = 'customer.index'
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for(index))
            else:
                flash('Wrong password. Please try again', 'danger')
        else:
            flash(f'The user {form.email.data} is not registered', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signupFunc():
    form = RegistrationForm()
    if request.method=="POST":
        if form.validate_on_submit(): 
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash(f'The user already exists, use another email.')
            else:
                if verify_password(form.password.data, user.password):
                    login_user(user, form.remember.data)
                    if user.has_role('admin'):
                        index = 'admin.index'
                    else:
                        index = 'customer.index'
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for(index))
                else:
                    flash('Wrong password. Please try again', 'danger')
    return render_template('signup.html', title='Signup', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/products', methods=["POST", "GET"])
def details():
    return render_template('allProducts.html', title='Products')