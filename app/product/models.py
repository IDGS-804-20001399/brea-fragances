from app import db

#admininistracion usuarios roles
#datos sensibles protegidos
# Trazabilidad cambios bases de datos, compra, pedidos
# cuando quien
# usuarios con los minimos privilegios en la bd y en la app
class ProductSupplies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'))
    quantity = db.Column(db.Float, nullable=False)
    supply = db.relationship('Supply', lazy=True, uselist=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    productSupplies = db.relationship('ProductSupplies', lazy=True, backref='product')