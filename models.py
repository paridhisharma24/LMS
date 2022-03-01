from flask_login import UserMixin
from sqlalchemy import null
from __init__ import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True,nullable=False)
    password = db.Column(db.String(20),nullable=False)
    name = db.Column(db.String(100),nullable=False)
    role = db.Column(db.Integer,nullable=False)
    salt = db.Column(db.String(20),nullable=False)