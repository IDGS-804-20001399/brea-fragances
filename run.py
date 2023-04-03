from app import create_app
from flask_wtf.csrf import CSRFProtect

csrf=CSRFProtect()
app = create_app()

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=True)
