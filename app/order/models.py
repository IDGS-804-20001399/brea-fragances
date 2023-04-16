from app import db
from sqlalchemy.ext.hybrid import hybrid_property

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment = db.Column(db.String(255), nullable=False)
    delivery_method = db.Column(db.String(255), nullable=False)
    delivery_fee = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', lazy=True, uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    details = db.relationship('OrderDetails', lazy=True)

    @hybrid_property
    def total(self):
        return sum([i.price * i.quantity for i in self.details])



class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.relationship('Order', lazy=True, uselist=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product = db.relationship('Product', lazy=True, uselist=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)