from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_security import login_required, current_user, roles_required

admin = Blueprint('admin', __name__,
                 template_folder='templates',
                 url_prefix='/admin')
            
@admin.route('/')
@login_required
@roles_required('admin')
def index():
    return render_template('admin.html', title='admin')