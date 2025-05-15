from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
import os 

# Base directory reading
basedir = os.path.abspath(os.path.dirname(__file__))


# Application configuration
app = Flask(__name__) 
app.config['SECRET_KEY'] = '/skde0(21349!23#41@@3#feo'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite') # 'sqlite:////tmp/test.db' 
# app.config['MAIL_SERVER'] = 'smtp.google.com'
# app.config['MAIL_PORT'] = '465'
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True



# Plugin initialization
db = SQLAlchemy() 
login_manager = LoginManager()


# App-Plugin initializaiton
db.init_app(app)
login_manager.init_app(app)
 



from app.store.views import store 
from app.auth.views import auth
app.register_blueprint(store)
app.register_blueprint(auth) 



with app.app_context():
    db.create_all() 