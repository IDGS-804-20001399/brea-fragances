from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, utils
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_session import Session
from app.config import Config
import os, logging

logging.basicConfig(filename='record.log',
                level=logging.CRITICAL)
db = SQLAlchemy()
product_pics =  UploadSet('products', IMAGES, lambda app: os.path.join(app.root_path, 'static/images/products'))
supply_pics =  UploadSet('supplies', IMAGES, lambda app: os.path.join(app.root_path, 'static/images/supplies'))
from app.auth.models import User, Role
from app.customer.models import Customer
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    configure_uploads(app, [product_pics, supply_pics])
    Session(app)

    from app.auth.routes import auth
    from app.product.routes import product
    from app.supply.routes import supply
    from app.customer.routes import customer
    from app.home.routes import home
    from app.supplier.routes import supplier
    from app.order.routes import order

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(product)
    app.register_blueprint(supply)
    app.register_blueprint(customer)
    app.register_blueprint(supplier)
    app.register_blueprint(order)

    security.init_app(app, user_datastore)
    with app.app_context():
        create_db()
    return app

def create_db():
    # Drop database
    # db.drop_all()
    # Creates the database
    db.create_all()
    # Creates the Roles "admin", "seller", "stocker", "customer" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='seller', description='Seller')
    user_datastore.find_or_create_role(name='stocker', description='Stocker')
    user_datastore.find_or_create_role(name='customer', description='Customer')

    # Encrypts the password
    encrypted_password = utils.encrypt_password('12345')
    # Creates the admin user if it doesn't exits yet
    if not user_datastore.get_user('admin@gmail.com'):
        user_datastore.create_user(email='admin@gmail.com', password=encrypted_password)
    db.session.commit()
    # Creates the stocker user if it doesn't exits yet
    if not user_datastore.get_user('stocker@gmail.com'):
        user_datastore.create_user(email='stocker@gmail.com', password=encrypted_password)
    db.session.commit()
    # Creates the seller user if it doesn't exits yet
    if not user_datastore.get_user('seller@gmail.com'):
        user_datastore.create_user(email='seller@gmail.com', password=encrypted_password)
    db.session.commit()
    # Creates the customer user if it doesn't exits yet
    if not user_datastore.get_user('customer@gmail.com'):
        user_datastore.create_user(email='customer@gmail.com', password=encrypted_password)
    db.session.commit()

    # Gives the "admin" role to the user admin if it doesn't have it yet
    user_datastore.add_role_to_user('admin@gmail.com', 'admin')
    # Gives the "seller" role to the user seller if it doesn't have it yet
    user_datastore.add_role_to_user('seller@gmail.com', 'seller')
    # Gives the "stocker" role to the user stocker if it doesn't have it yet
    user_datastore.add_role_to_user('stocker@gmail.com', 'stocker')
    # Gives the "customer" role to the user admin if it doesn't have it yet
    user_datastore.add_role_to_user('customer@gmail.com', 'customer')
    db.session.commit()

    # Adding a customer
    if not Customer.query.get(1):
        customer_user = user_datastore.get_user('customer@gmail.com')
        customer = Customer(names = "Roberto Carlos", 
                            lastnames="Aguilera Alcantar",
                            address="Santa cruz #129",
                            phone="4774008971",
                            user = customer_user)
        db.session.add(customer)
        db.session.commit()