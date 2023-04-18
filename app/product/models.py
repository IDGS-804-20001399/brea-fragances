from app import db
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import math
from datetime import datetime, date

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
    makes = db.relationship('ProductInventory', lazy='dynamic', backref='product')

    @hybrid_property
    def make_records(self):
        return self.makes.order_by(ProductInventory.creation_date.desc()).all()

    @hybrid_property
    def inventory(self):
        return self.makes.filter(ProductInventory.expiration_date > date.today()).order_by(ProductInventory.expiration_date).all()

    @hybrid_property
    def stock(self):
        buys = self.makes.filter(ProductInventory.expiration_date > date.today()).all()
        stock = sum([i.available_quantity for i in buys])
        return stock


    @hybrid_property
    def production_cost(self):
        return sum([i.quantity_cost for i in self.productSupplies])

    @hybrid_method
    def can_produce(self, quantity: int) -> list:
        missing = []
        for supply in self.productSupplies:
            quantity_needed = supply.quantity * quantity
            quantity_in_stock = supply.supply.stock_in_use_unit
            missing_quantity = quantity_needed - quantity_in_stock
            buy_missing_quantity = math.ceil(missing_quantity / supply.supply.equivalence)
            if missing_quantity > 0:
                missing.append({
                    'name': supply.supply.name,
                    'missing': missing_quantity,
                    'buy_missing': buy_missing_quantity,
                    'buy_unit': supply.supply.buy_unit,
                    'use_unit': supply.supply.use_unit
                })
        return missing


    


class ProductInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiration_date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    @hybrid_property
    def total_cost(self):
        return self.unit_cost * self.quantity
