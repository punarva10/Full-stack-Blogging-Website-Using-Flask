from datetime import datetime
from re import S
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager
from flask_login import UserMixin   #something that manages a few models required for login
from flask import current_app

@login_manager.user_loader               #decorator function that's required for the  
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): #these classes are called models
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),  unique=True, nullable=False)
    email = db.Column(db.String(120),  unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True) #creating a one-to-many relationship with Post; backref is used to get info about the author of a certain post; lazy defines when SQLAlchemy loads the data from the database # P is uppercase as we're referencing the actual Post class

    def get_reset_token(self, expires_sec = 120):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod #to tell python im not going to be passing in self in the arguments
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self): #how our object is printed when it is printed out
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #user is lowercase because we are referencing the default created table name in ForeignKey

    def __repr__(self): #how our object is printed when it is printed out
        return f"Post('{self.title}', '{self.date_posted}')"