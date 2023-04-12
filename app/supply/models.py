from app import db

class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    buy_unit = db.Column(db.String(60), nullable=False)
    use_unit = db.Column(db.String(60), nullable=False)
    equivalence = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(255))
    image_url = db.Column(db.String(255))


class SupplyInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buy_date = db.Column(db.DateTime, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'), nullable=False)