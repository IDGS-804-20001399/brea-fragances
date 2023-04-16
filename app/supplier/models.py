from app import db

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(60), nullable=False)
    product = db.Column(db.String(60), nullable=False)


# class SupplyInventory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     buy_date = db.Column(db.DateTime, nullable=False)
#     expiration_date = db.Column(db.DateTime, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     total_cost = db.Column(db.Float, nullable=False)
#     unit_cost = db.Column(db.Float, nullable=False)
#     supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'), nullable=False)