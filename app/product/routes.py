import os, json
from flask import (render_template, url_for, flash, redirect, 
                    request, Blueprint)
from flask_security import login_required, roles_required
from app.product.forms import ProductForm
from app.product.models import Product, ProductSupplies
from app.supply.models import Supply
from app import product_pics, db


product = Blueprint('product', __name__,
                 template_folder='templates',
                 url_prefix='/admin')


@product.route('/products')
@login_required
@roles_required('admin')
def products():
    products = Product.query.all()
    return render_template('products.html', title='Products', products=products)


@product.route('/add-product', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def add_product():
    form=ProductForm()
    default_image = url_for('static', filename='images/preview.png')
    supplies = Supply.query.all()
    if form.validate_on_submit():
        try:
            supplies_data = json.loads(form.supplies.data)
            if len(supplies_data) > 0:
                if form.image.data:
                    product = Product(
                        name = form.name.data,
                        description = form.description.data,
                        price = form.price.data
                    )
                    db.session.add(product)
                    db.session.commit()

                    for supply in supplies_data:
                        productSupplies = ProductSupplies(
                            product_id = product.id,
                            supply_id = supply['id'],
                            quantity = supply['amount']
                        )
                        db.session.add(productSupplies)



                    image_filename = product_pics.save(form.image.data, name=f'{product.id}.')
                    image_url = url_for(
                        "_uploads.uploaded_file", 
                        setname=product_pics.name, 
                        filename=image_filename
                    )
                    product.image_filename = image_filename
                    product.image_url = image_url
                    db.session.commit()
                    flash('Product saved successfully', 'success')
                    return redirect(url_for("product.products"))
                else:
                    flash('Please select an image', 'danger')
            else:
                flash('Please select some suplies', 'danger')
        except:
            flash('Invalid supplies format', 'danger')
    return render_template('addProduct.html', title='Add Product', form=form, default_image = default_image, supplies=supplies)


@product.route('/edit-product/<int:product_id>', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    allSupplies = Supply.query.all()
    productSupplies = ProductSupplies.query.filter_by(product_id=product.id).all()
    suppliesData = []
    quantities = []
    ids =[]
    for item in productSupplies:
        suppliesData.append(Supply.query.filter_by(id=item.supply_id).first())
        quantities.append(item.quantity)
        ids.append(item.supply_id)

    form = ProductForm()
    default_image = product.image_url
    
    if form.validate_on_submit():
        try:
            supplies_data = json.loads(form.supplies.data)
            if len(supplies_data) > 0:
                if form.image.data:
                    product.name = form.name.data
                    print("\033[1m"+"\033[95m"+"==>> product: " + "\033[96m", product.id)
                    product.description = form.description.data
                    product.price = form.price.data
                    if form.image.data:
                        previos_image_path = product_pics.path(product.image_filename)
                        try:
                            os.remove(previos_image_path)
                        except:
                            pass
                        image_filename = product_pics.save(form.image.data, name=f'{product.id}.')
                        image_url = url_for(
                            "_uploads.uploaded_file", 
                            setname=product_pics.name, 
                            filename=image_filename
                        )
                        product.image_filename = image_filename
                        product.image_url = image_url

                    newSupplies = []
                    for element in supplies_data:
                        if element['id'] not in ids:
                            newSupplies.append(int(element['id']))

                    sameSupplies = []
                    for element in supplies_data:
                        if int(element['id']) in ids:
                            sameSupplies.append(int(element['id']))
                    
                    deleteSupplies = []
                    for element in ids:
                        if element not in sameSupplies and element not in newSupplies:
                            deleteSupplies.append(element)

                    for supply in supplies_data:
                        if supply['id'] not in sameSupplies and supply['id'] in newSupplies:
                            productSupplies = ProductSupplies(
                                product_id = product.id,
                                supply_id = supply['id'],
                                quantity = supply['amount'])
                            db.session.add(productSupplies)

                        elif supply['id'] in sameSupplies and supply['id'] in newSupplies:
                            obj = ProductSupplies.query.where(supply_id=supply['id'], product_id=product.id)
                            obj.quantity = supply['amount']
                            
                        if supply['id'] in deleteSupplies:
                            obj = ProductSupplies.query.where(supply_id=supply['id'], product_id=product.id)
                            db.session.delete(obj)
                        

                    db.session.commit()
                    flash('Product saved successfully', 'success')
                    return redirect(url_for("product.products"))
                else:
                    flash('Please select an image', 'danger')
            else:
                flash('Please select some suplies', 'danger')
        except:
            flash('Invalid supplies format', 'danger')
    elif request.method == 'GET':
        form.name.data = product.name
        form.price.data = product.price
        form.description.data = product.description
    return render_template('addProduct.html', ids=ids,allSupplies=allSupplies, quantities=quantities, title='Edit Product', form=form, default_image = default_image)


@product.route('/delete-product/<int:product_id>', methods=["POST"])
@login_required
@roles_required('admin')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    previos_image_path = product_pics.path(product.image_filename)
    try:
        os.remove(previos_image_path)
    except:
        pass
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('product.products'))

@product.route('/product-info/<int:product_id>', methods=["POST", "GET"])
@login_required
def productInfo(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('singleProduct.html', title='Details', product=product)

@product.route('/products/search', methods=["POST", "GET"])
@login_required
def search():
    word = request.form.get('search')
    if(word != None and word !=''):
        search="%{}%".format(word)
        products = Product.query.filter(Product.name.like(search)).all()

        return render_template('search.html', title='Results of "'+word+'"', products=products)
    
    return render_template('search.html', title='No results')

@product.route('/product-details/<int:product_id>', methods=["POST", "GET"])
@login_required
@roles_required('admin')
def details(product_id):
    product = Product.query.get_or_404(product_id)
    productSupplies = ProductSupplies.query.filter_by(product_id=product.id).all()
    supplies = []
    quantities = []
    for item in productSupplies:
        supplies.append(Supply.query.filter_by(id=item.supply_id).first())
        quantities.append(item.quantity)
    return render_template('productDetails.html', title='Details', 
                           product=product, supplies=supplies, quantities=quantities, productSupplies=productSupplies)