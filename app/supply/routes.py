import os
from flask import (render_template, url_for, flash, redirect, 
                    request, Blueprint)
from flask_security import login_required, roles_required
from app.supply.forms import SupplyForm
from app.supply.models import Supply
from app import supply_pics, db

supply = Blueprint('supply', __name__,
                 template_folder='templates',
                 url_prefix='/admin')

@supply.route('/supplies')
@login_required
@roles_required('admin')
def supplies():
    supplies = Supply.query.all()
    return render_template('supplies.html', title='Supplies', supplies=supplies)


@supply.route('/supply-inventory')
@login_required
@roles_required('admin')
def inventory():
#     select s.*, i.buy_date, i.expiration_date, 
# sum(i.quantity) stock_buy_unit,
# sum(i.quantity) * s.equivalence stock_use_unit
# from supply s 
# inner join supply_inventory i on s.id = i.supply_id 
# group by s.id;
    pass


@supply.route('/add-supply', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def add_supply():
    form=SupplyForm()
    default_image = url_for('static', filename='images/preview.png')
    if form.validate_on_submit():
        if form.image.data:
            supply = Supply(
                name = form.name.data,
                cost = form.cost.data,
                buy_unit = form.buy_unit.data,
                use_unit = form.use_unit.data,
                equivalence = form.equivalence.data
            )
            db.session.add(supply)
            db.session.commit()
            image_filename = supply_pics.save(form.image.data, name=f'{supply.id}.')
            image_url = url_for(
                "_uploads.uploaded_file", 
                setname=supply_pics.name, 
                filename=image_filename
            )
            supply.image_filename = image_filename
            supply.image_url = image_url
            db.session.commit()
            flash('Supply saved successfully', 'success')
            return redirect(url_for("supply.supplies"))
        else:
            flash('Please select an image', 'danger')
    return render_template('addSupply.html', title='Add Supply', form=form, default_image = default_image)


@supply.route('/edit-supply/<int:supply_id>', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def edit_supply(supply_id):
    supply = Supply.query.get_or_404(supply_id)
    form = SupplyForm()
    default_image = supply.image_url
    if form.validate_on_submit():
        supply.name = form.name.data
        supply.cost = form.cost.data
        supply.buy_unit = form.buy_unit.data
        supply.use_unit = form.use_unit.data
        supply.equivalence = form.equivalence.data
        if form.image.data:
            previos_image_path = supply_pics.path(supply.image_filename)
            try:
                os.remove(previos_image_path)
            except:
                pass
            image_filename = supply_pics.save(form.image.data, name=f'{supply.id}.')
            image_url = url_for(
                "_uploads.uploaded_file", 
                setname=supply_pics.name, 
                filename=image_filename
            )
            supply.image_filename = image_filename
            supply.image_url = image_url
        db.session.commit()
        flash('Supply saved successfully', 'success')
        return redirect(url_for('supply.supplies'))
    elif request.method == 'GET':
        form.name.data = supply.name
        form.cost.data = supply.cost
        form.buy_unit.data = supply.buy_unit
        form.use_unit.data = supply.use_unit
        form.equivalence.data = supply.equivalence
    return render_template('addSupply.html', title='Edit supply', form=form, default_image = default_image)


@supply.route('/delete-supply/<int:supply_id>', methods=["POST"])
@login_required
@roles_required('admin')
def delete_supply(supply_id):
    supply = Supply.query.get_or_404(supply_id)
    previos_image_path = supply_pics.path(supply.image_filename)
    try:
        os.remove(previos_image_path)
    except:
        pass
    db.session.delete(supply)
    db.session.commit()
    flash('Supply deleted successfully', 'success')
    return redirect(url_for('supply.supplies'))