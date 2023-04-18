from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from datetime import date

class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    buy_unit = db.Column(db.String(60), nullable=False)
    use_unit = db.Column(db.String(60), nullable=False)
    equivalence = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    buys = db.relationship('SupplyBuys', lazy='dynamic', backref='supply')

    @hybrid_property
    def buy_records(self):
        return self.buys.order_by(SupplyBuys.buy_date.desc()).all()

    @hybrid_property
    def inventory(self):
        return self.buys.filter(SupplyBuys.expiration_date > date.today()).order_by(SupplyBuys.expiration_date).all()

    @hybrid_property
    def stock(self):
        buys = self.buys.filter(SupplyBuys.expiration_date > date.today()).all()
        stock = sum([i.available_quantity for i in buys])
        return stock

    @hybrid_property
    def stock_in_use_unit(self):
        buys = self.buys.filter(SupplyBuys.expiration_date > date.today()).all()
        stock = sum([i.available_use_quantity for i in buys])
        return stock





class SupplyBuys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buy_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiration_date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    available_use_quantity = db.Column(db.Float, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'), nullable=False)

    @hybrid_property
    def available_quantity(self):
        return self.available_use_quantity / self.supply.equivalence


    @hybrid_property
    def total_cost(self):
        return self.unit_cost * self.quantity