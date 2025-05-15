from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
 
class Book(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(255)) 
    price = db.Column(db.Float) 
    image_path = db.Column(db.String(255)) 
    category_id = db.Column(db.Integer, db.ForeignKey('category.id')) 
    category = db.relationship('Category', backref=db.backref('books', lazy='dynamic')) 
 
    def __init__(self, name, price, category, image_path): 
        self.name = name 
        self.price = price 
        self.category = category 
        self.image_path = image_path 
 
    def __repr__(self): 
        return '<Product %d>' % self.id 
    
class Category(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100)) 
 
    def __init__(self, name): 
        self.name = name 
 
    def __repr__(self): 
        return '<Category %d>' % self.id 
 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # Basics
    id            = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(64), nullable = False, default='default_profile.jpg') # Might delete this in future
    email         = db.Column(db.String(64), unique=True, index=True)
    username      = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # Roles
    role = db.Column(db.String(64), default=None)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"



# full_name = StringField('Full Name', validators=[InputRequired()])
#     email = StringField('Email', validators=[InputRequired()])
#     address = StringField('Address', validators=[InputRequired()])
#     city =

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    address = db.Column(db.String(128))
    items = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.Float)
    status = db.Column(db.String(20), default='processing') # processing/delivered

    user = db.relationship('User', backref=db.backref('orders', lazy=True))

    def __init__(self, name, email, address, city, items, user_id, price):
        self.name = name
        self.email = email
        self.address = address
        self.city = city
        self.items = items
        self.user_id = user_id
        self.price = price
