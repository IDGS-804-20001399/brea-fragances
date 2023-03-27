from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, utils
from app.config import Config

db = SQLAlchemy()
from app.auth.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app.auth.routes import auth
    from app.admin.routes import admin
    from app.customer.routes import customer
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(customer)

    security.init_app(app, user_datastore)
    with app.app_context():
        create_db()
    # from flaskblog.users.routes import users
    # from flaskblog.posts.routes import posts
    # from flaskblog.main.routes import main
    # app.register_blueprint(users)
    # app.register_blueprint(posts)
    # app.register_blueprint(main)
    return app

def create_db():
    # Creates the database
    db.create_all()
    # Creates the Roles "admin" and "customer" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='customer', description='Customer')

    # Encrypts the password
    encrypted_password = utils.encrypt_password('12345')
    # Creates the admin user if it doesn't exits yet
    if not user_datastore.get_user('admin@gmail.com'):
        user_datastore.create_user(email='admin@gmail.com', password=encrypted_password)
    db.session.commit()
    # Creates the customer user if it doesn't exits yet
    if not user_datastore.get_user('customer@gmail.com'):
        user_datastore.create_user(email='customer@gmail.com', password=encrypted_password)
    db.session.commit()

    # Gives the "admin" role to the user admin if it doesn't have it yet
    user_datastore.add_role_to_user('admin@gmail.com', 'admin')
    # Gives the "customer" role to the user admin if it doesn't have it yet
    user_datastore.add_role_to_user('customer@gmail.com', 'customer')
    db.session.commit()