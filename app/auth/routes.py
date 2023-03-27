from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.auth.forms import LoginForm
from app.auth.models import User
from flask_security.utils import encrypt_password, verify_password, login_user, logout_user
from flask_security import login_required 

auth = Blueprint('auth', __name__,
                 template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
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

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))