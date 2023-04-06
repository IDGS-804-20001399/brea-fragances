from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(100), nullable=False)
    lastnames = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    user = db.relationship('User', lazy=True, uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))