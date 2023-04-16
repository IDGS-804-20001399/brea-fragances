from app import db
from sqlalchemy.ext.hybrid import hybrid_property

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

    @hybrid_property
    def quantity_cost(self):
        return self.supply.cost / self.supply.equivalence * self.quantity


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    productSupplies = db.relationship('ProductSupplies', lazy=True, backref='product')


    @hybrid_property
    def production_cost(self):
        return sum([i.quantity_cost for i in self.productSupplies])


class ProductInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    @hybrid_property
    def total_cost(self):
        return self.unit_cost * self.quantity
