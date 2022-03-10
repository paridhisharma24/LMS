from flask import Flask
from __init__ import db
from flask_login import UserMixin


class user_roles(UserMixin,db.Model):
    __tablename__ = 'user_roles'

    role = db.Column(
        db.String(10),
        primary_key=True
    )
    role_name = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )
    details = db.relationship('user_details')


class user_details(UserMixin,db.Model):
    __tablename__ = 'user_details'
    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )
    
    phone_no = db.Column(
        db.String(10),
        nullable=False
    )

    dob = db.Column(
        db.Date,
        nullable=True
    )

    address = db.Column(
        db.String(150),
        nullable=True
    )

    user_id = db.Column(
        db.Integer, 
        primary_key=True
    ) 

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(20),
        nullable=False
    )
                
    role = db.Column(
        db.String(10),
        db.ForeignKey('user_roles.role')
    )

    salt = db.Column(
        db.String(20),
        nullable=False
    )
    student = db.relationship('course_students')
    mentor = db.relationship('course_mentors')


class course_details(UserMixin,db.Model):
    __tablename__ = 'course_details'
    course_id = db.Column(
        db.String(20),
        nullable=False,
        primary_key=True
    )

    course_name = db.Column(
        db.String(50),
        nullable=False
    )
    content = db.relationship('course_content')
    students = db.relationship('course_students')
    mentor = db.relationship('course_mentors')


class content_types(UserMixin,db.Model):
    __tablename__ = 'content_types' 
    content_id = db.Column(
        db.String(20),
        nullable=False,
        primary_key = True
    )
    ass_name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    content = db.relationship('course_content')


class course_content(UserMixin,db.Model):
    __tablename__ = 'course_content'
    date_of_upload = db.Column(
        db.Date,
        nullable=True
    )

    course_id = db.Column(
        db.String(20),
        db.ForeignKey('course_details.course_id'),
        primary_key = True
    )
    
    content_type = db.Column(
        db.String(20),
        db.ForeignKey('content_types.content_id')
    )

    link = db.Column(
        db.String(150),
        nullable=False
    )


class course_students(UserMixin,db.Model):
    __tablename__ = 'course_students'

    course_id = db.Column(
        db.String(20),
        db.ForeignKey('course_details.course_id'),
        primary_key = True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_details.user_id')
    )
   # course_grade =db.Column(
       # db.Integer,
       # nullable =True)
    


class course_mentors(db.Model):
    __tablename__ = 'course_mentors'

    course_id = db.Column(
        db.String(20),
        db.ForeignKey('course_details.course_id'),
        primary_key = True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_details.user_id')
    )

class Upload(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    course_id=db.Column(db.String)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)