from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restx import Api

# Flask application initialization
app = Flask(__name__)
app.config.from_object(Config)

# Database initialization
db = MongoEngine()
db.init_app(app)

# Api initialization
api = Api()
api.init_app(app)

from application import routes