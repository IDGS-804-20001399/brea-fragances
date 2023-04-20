import os
from flask import (render_template, url_for, flash, redirect, 
                    request, Blueprint, current_app)
from flask_security import login_required, roles_required, current_user
from app.supplier.forms import SupplierForm
from app.supplier.models import Supplier
from app import db

supplier = Blueprint('supplier', __name__,
                 template_folder='templates',
                 url_prefix='/admin')

@supplier.route('/suppliers')
@login_required
@roles_required('admin')
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', title='Suppliers', suppliers=suppliers)


@supplier.route('/add-supplier', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def add_supplier():
    form=SupplierForm()
    default_image = url_for('static', filename='images/preview.png')
    if form.validate_on_submit():
        if form.image.data:
            supplier = Supplier(
                name = form.name.data,
                contact = form.contact.data,
                product = form.product.data
            )
            db.session.add(supplier)
            db.session.commit()
            current_app.logger.critical(f"SUPPLIER {supplier.name} ADDED BY {current_user.email}")
            flash('Supplier saved successfully', 'success')
            return redirect(url_for("supplier.supplies"))
        else:
            flash('Please select an image', 'danger')
    return render_template('addSupplier.html', title='Add Supplier', form=form)


@supplier.route('/edit-supplier/<int:supplier_id>', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def edit_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    form = SupplierForm()
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.email = form.email.data
        supplier.phone = form.phone.data
        supplier.product = form.product.data
        db.session.commit()
        flash('Supplier saved successfully', 'success')
        current_app.logger.critical(f"SUPPLIER {supplier.name} MODIFIED BY {current_user.email}")
        return redirect(url_for('supplier.supplies'))
    elif request.method == 'GET':
        form.name.data = supplier.name
        form.email.data = supplier.email
        form.phone.data = supplier.phone
        form.product.data = supplier.product
    return render_template('addSupplier.html', title='Edit supplier', form=form)


@supplier.route('/delete-supplier/<int:supplier_id>', methods=["POST"])
@login_required
@roles_required('admin')
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    current_app.logger.critical(f"SUPPLIER {supplier.name} DELETED BY {current_user.email}")
    flash('Supplier deleted successfully', 'success')
    return redirect(url_for('supplier.supplies'))