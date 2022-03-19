from flask import Flask
from __init__ import db
from flask_login import UserMixin

#available user roles: Admin, Mentor, Mentee 
class UserRoles(UserMixin, db.Model):
    __tablename__ = 'UserRoles'

    role = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    role_name = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )
    login = db.relationship('LoginDetails')
    #dictionary to map roles to id


class LoginDetails(UserMixin, db.Model):
    __tablename__ = 'LoginDetails'

    user_id = db.Column(
        db.Integer, 
        primary_key=True,
        autoincrement=True
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

    salt = db.Column(
        db.String(20),
        nullable=False
    )
    
    role = db.Column(
        db.Integer,
        db.ForeignKey('UserRoles.role'),
        nullable = False
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    user = db.relationship('User')


#user specific details
class User(UserMixin,db.Model):
    __tablename__ = 'User'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('LoginDetails.user_id'),
        primary_key=True
    )

    # first_name = db.Column(
    #     db.String(100),
    #     nullable=False
    # )

    # last_name = db.Column(
    #     db.String(100),
    #     nullable=False
    # )
    
    dob = db.Column(
        db.Date,
        nullable=True
    )

    phone_no = db.relationship('PhoneNo')
    address = db.relationship('Address')
    student = db.relationship('CourseStudents')
    mentor = db.relationship('CourseInstance')
    mentor_content = db.relationship('MentorContent')


#phone numbers of users
class PhoneNo(UserMixin, db.Model):
    __tablename__ = 'PhoneNo'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id'),
        primary_key=True
    )
    phone = db.Column(
        db.String(15),
        nullable=False,
        primary_key=True
    )


#address of user
class Address(UserMixin, db.Model):
    __tablename__ = 'Address'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id'),
        primary_key=True
    )

    house_no = db.Column(
        db.Integer,
        nullable=False
    )

    street = db.Column(
        db.String(20),
        nullable=True
    )

    locality = db.Column(
        db.String(50),
        nullable=False
    )

    city = db.Column(
        db.String(50),
        nullable=False
    )

    state = db.Column(
        db.String(50),
        nullable=False
    )

    pincode= db.Column(
        db.Integer,
        nullable=False
    )

    country = db.Column(
        db.String(50),
        nullable=False
    )


#Available courses 
class Course(UserMixin,db.Model):
    __tablename__ = 'Course'
    course_id = db.Column(
        db.Integer,
        nullable=False,
        primary_key=True
    )

    course_name = db.Column(
        db.String(50),
        nullable=False
    )
    content = db.relationship('MentorContent')
    students = db.relationship('CourseStudents')
    mentor = db.relationship('CourseInstance')


#types of content like Assignment, notes, lecture, etc.
class ContentTypes(UserMixin,db.Model):
    __tablename__ = 'ContentTypes' 

    content_id = db.Column(
        db.Integer,
        nullable=False,
        primary_key = True,
        autoincrement=True 
    )

    content_name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    content = db.relationship('MentorContent')


#contents of a course uploaded by a mentor - Assignment, Notes
class MentorContent(UserMixin,db.Model):
    __tablename__ = 'MentorContent'

    content_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement=True
    )

    mentor_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id')
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('Course.course_id')
    )

    upload_date = db.Column(
        db.Date,
        nullable=True
    )

    due_date = db.Column(
        db.Date,
        nullable=True
    )
    
    type = db.Column(
        db.Integer,
        db.ForeignKey('ContentTypes.content_id')
    )

    data = db.Column(
        db.LargeBinary,
        nullable=False
    )
    assignment = db.relationship('MenteeAssignment')


#student and course mapping
class CourseStudents(UserMixin,db.Model):
    __tablename__ = 'Course_Students'

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('Course.course_id'),
        primary_key = True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id'),
        primary_key = True
    )

    grade = db.Column(
        db.String(10),
        nullable=True
    )


#course and mentor mapping
class CourseInstance(db.Model):
    __tablename__ = 'CourseInstance'

    instance_id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key = True
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('Course.course_id')
    )

    mentor_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id')
    )

    start_date = db.Column(
        db.Date,
        nullable=True
    )

    end_date = db.Column(
        db.Date,
        nullable=True
    )

    # upload_date = db.Column(
    #     db.Date,
    #     nullable=True
    # )


#details of assignment uploaded by students/mentees
#mentee - assignment

class MenteeAssignment(db.Model):  #submission
    __tablename__ = 'MenteeAssignment'

    assignment_id = db.Column(
        db.Integer,
        db.ForeignKey('MentorContent.content_id'),
        primary_key = True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id'),
        primary_key = True
    )
    
    data = db.Column(
        db.LargeBinary,
        nullable=False
    )

    filename = db.Column(
        db.String(30),
        nullable = False
    )

    grade = db.Column(
        db.String(10),
        nullable=True
    )
