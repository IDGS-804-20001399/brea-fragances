from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.auth.forms import LoginForm, RegistrationForm, AdminForm
from app.auth.models import User, Role
from app.customer.models import Customer
from flask_security.utils import encrypt_password, verify_password, login_user, logout_user
from flask_security import login_required 
from app import user_datastore, db
from flask_security import login_required, roles_required

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
                    index = 'home.index'
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
    if form.validate_on_submit(): 
        encrypted_password = encrypt_password(form.password.data)
        customer_user = user_datastore.create_user(email=form.email.data, password=encrypted_password)
        db.session.commit()
        user_datastore.add_role_to_user(form.email.data, 'customer')
        customer = Customer(names=form.names.data, 
                            lastnames=form.lastnames.data,
                            address=form.address.data,
                            phone=form.phone.data,
                            user = customer_user)
        db.session.add(customer)
        db.session.commit()
        flash('Registration completed. Now log in', 'success')
        return redirect(url_for('auth.loginFunc'))
    return render_template('signup.html', title='Signup', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.loginFunc'))

@auth.route('/users')
@login_required
@roles_required( 'admin')
def users():
    users = User.query.all()
    return render_template('users.html', title='Users', users=users)

@auth.route('/add-user')
@login_required
@roles_required( 'admin')
def add_user():
    form = AdminForm()
    return render_template('addUser.html', title='User', form=form)

@auth.route('/edit-user')
@login_required
@roles_required( 'admin')
def edit_user():
    form = AdminForm()
    roles = Role.query.all()
    return render_template('addUser.html', title='User', roles=roles, form=form)
