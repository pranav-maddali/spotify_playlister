from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    #user_id should be the primary key in our database
    id = db.Column(db.Integer, primary_key=True)
