from flask import Flask
from __init__ import db
from flask_login import UserMixin


class UserRoles(UserMixin,db.Model):
    __tablename__ = 'UserRoles'

    role = db.Column(
        db.String(10),
        primary_key=True
    )
    role_name = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )
    details = db.relationship('User')


class User(UserMixin,db.Model):
    __tablename__ = 'User'
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
        db.ForeignKey('UserRoles.role')
    )

    salt = db.Column(
        db.String(20),
        nullable=False
    )
    student = db.relationship('Course_Students')
    mentor = db.relationship('Course_Mentors')


class Course(UserMixin,db.Model):
    __tablename__ = 'Course'
    course_id = db.Column(
        db.String(20),
        nullable=False,
        primary_key=True
    )

    course_name = db.Column(
        db.String(50),
        nullable=False
    )
    content = db.relationship('Contents')
    students = db.relationship('Course_Students')
    mentor = db.relationship('Course_Mentors')


class ContentTypes(UserMixin,db.Model):
    __tablename__ = 'ContentTypes' 
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
    content = db.relationship('Contents')


class Contents(UserMixin,db.Model):
    __tablename__ = 'Contents'
    date_of_upload = db.Column(
        db.Date,
        nullable=True
    )

    course_id = db.Column(
        db.String(20),
        db.ForeignKey('Course.course_id'),
        primary_key = True
    )
    
    content_type = db.Column(
        db.String(20),
        db.ForeignKey('ContentTypes.content_id')
    )

    link = db.Column(
        db.String(150),
        nullable=False
    )


class Course_Students(UserMixin,db.Model):
    __tablename__ = 'Course_Students'

    course_id = db.Column(
        db.String(20),
        db.ForeignKey('Course.course_id'),
        primary_key = True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id')
    )


class Course_Mentors(db.Model):
    __tablename__ = 'Course_Mentors'

    course_id = db.Column(
        db.String(20),
        db.ForeignKey('Course.course_id'),
        primary_key = True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id')
    )