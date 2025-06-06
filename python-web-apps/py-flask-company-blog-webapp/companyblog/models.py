from companyblog import db # import db from the __init__.py file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from companyblog import login_manager # import login_manager from __init__.py
from datetime import datetime # datetime for python


# Login manager setup - see __init__.py
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# User model 
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(64), nullable = False, default='default_profile.jpg')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # The author of a blog post is the user model
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"


# Blog post mdoel
class BlogPost(db.Model):
    
    __tablename__ = 'blogposts'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable= False)
    text = db.Column(db.Text, nullable = False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"POST ID: {self.id} -- Date: {self.date} -- Title: {self.title}"

