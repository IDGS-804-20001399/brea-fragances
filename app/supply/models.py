from app import db
from sqlalchemy.ext.hybrid import hybrid_property

class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    buy_unit = db.Column(db.String(60), nullable=False)
    use_unit = db.Column(db.String(60), nullable=False)
    equivalence = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(255))
    image_url = db.Column(db.String(255))


class SupplyBuys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buy_date = db.Column(db.DateTime, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    available_use_quantity = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'), nullable=False)
    supply = db.relationship('Supply', lazy=True, uselist=False)

    @hybrid_property
    def available_quantity(self):
        return self.available_use_quantity / self.supply.equivalence


    @hybrid_property
    def unit_cost(self):
        return self.total_cost / self.quantity