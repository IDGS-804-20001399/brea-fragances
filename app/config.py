class Config:
    SECRET_KEY = "this is a secret"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1/fragance_db";
    SECURITY_PASSWORD_SALT = "this is a security salt"
    UPLOADS_AUTOSERVE = True
    DEBUG = True