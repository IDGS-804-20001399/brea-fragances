from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.auth.forms import LoginForm, RegistrationForm, AdminForm, EmailForm, PasswordForm
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

@auth.route('/add-user', methods=['GET', 'POST'])
@login_required
@roles_required( 'admin')
def add_user():
    form = AdminForm()
    roles = Role.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            encrypted_password = encrypt_password(form.password.data)
            user = user_datastore.create_user(email=form.email.data, password=encrypted_password)
            db.session.add(user)
            user_datastore.add_role_to_user(form.email.data, request.form.get('role'))
            db.session.commit()
            flash('User saved successfully', 'success')
            return redirect(url_for("auth.users"))

    return render_template('addUser.html', title='User', roles=roles, form=form)

@auth.route('/edit-user-role/<int:user_id>', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def edit_user_role(user_id):
    form = AdminForm()
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()

    if request.method=='POST':
        user_datastore.remove_role_from_user(user.email, user.roles[0].name)
        user_datastore.add_role_to_user(user.email, request.form.get('role'))
        db.session.commit()
        flash('User saved successfully', 'success')
        return redirect(url_for('auth.users'))
    elif request.method == 'GET':
        form.email.data = user.email
    return render_template('editRole.html', title='User', roles=roles, form=form)

@auth.route('/edit-user-email/<int:user_id>', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def edit_user_email(user_id):
    form = EmailForm()
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()

    if request.method=='POST':
        if form.validate_on_submit() and user.email != form.email.data:
            user.email = form.email.data
            db.session.commit()
            flash('Email changed successfully', 'success')
            return redirect(url_for('auth.users'))
        else:
            flash('This email is already taken', 'danger')
    elif request.method == 'GET':
        form.email.data = user.email
    return render_template('editEmail.html', title='User', roles=roles, form=form)

@auth.route('/edit-user-password/<int:user_id>', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def edit_user_password(user_id):
    form = PasswordForm()
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    
    if request.method=='POST':
        if form.current_password.data == user.password and form.validate_on_submit():
            user.password = form.new_password.data
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('auth.users'))
    return render_template('editPassword.html', title='User', roles=roles, form=form)

@auth.route('/delete-user/<int:user_id>', methods=["POST"])
@login_required
@roles_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('auth.users'))