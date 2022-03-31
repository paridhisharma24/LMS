from fileinput import filename
from flask import Flask
from __init__ import db
from flask_login import UserMixin
from datetime import datetime

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
    #login = db.relationship('LoginDetails')


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
    dob = db.Column(
        db.Date,
        nullable=True
    )
    phone_no = db.relationship('PhoneNo')
    address = db.relationship('Address')
    #student = db.relationship('CourseStudents')
    #mentor = db.relationship('CourseInstance')
    posts = db.relationship('Post', backref = 'author', lazy = True)
    replies = db.relationship('Reply', backref = 'user', lazy = True)
    


#phone numbers of users
class PhoneNo(UserMixin, db.Model):
    __tablename__ = 'PhoneNo'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('LoginDetails.user_id'),
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
        db.ForeignKey('LoginDetails.user_id'),
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
        nullable=True
    )

    city = db.Column(
        db.String(50),
        nullable=True
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
    #content = db.relationship('MentorContent')
    #instance = db.relationship('CourseInstance')


#types of content like Assignment, notes, lecture, etc.
class ContentTypes(UserMixin,db.Model):
    __tablename__ = 'ContentTypes' 

    type = db.Column(
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

#course and mentor mapping
class CourseInstance(db.Model):
    __tablename__ = 'CourseInstance'

    instance_id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key = True
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('LoginDetails.user_id')
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('Course.course_id')
    )

    start_date = db.Column(
        db.Date,
        nullable=True
    )

    end_date = db.Column(
        db.Date,
        nullable=True
    )

    upload_date = db.Column(
        db.Date,
        nullable=True
    )
    
    #mentor_content = db.relationship('MentorContent')


#contents of a course uploaded by a mentor - Assignment, Notes
class MentorContent(UserMixin,db.Model):
    __tablename__ = 'MentorContent'

    content_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('CourseInstance.user_id')
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('Course.course_id'),
        nullable = False
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
        db.ForeignKey('ContentTypes.type'),
        nullable = False
    )

    data = db.Column(
        db.LargeBinary,
        nullable=False
    )
    
    filename=db.Column(
        db.String(50),
        nullable=False
    )
    #assignment = db.relationship('MenteeAssignment')


#student and course mapping
class CourseStudents(UserMixin,db.Model):
    __tablename__ = 'CourseStudents'

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('Course.course_id'),
        primary_key = True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('LoginDetails.user_id'),
        primary_key = True
    )

    grade = db.Column(
        db.String(10),
        nullable=True
    )
    #grade_assignment = db.relationship('Grade')



#details of assignment uploaded by students/mentees
class MenteeAssignment(db.Model):  #submission
    __tablename__ = 'MenteeAssignment'

    upload_id = db.Column(
        db.Integer,
        nullable=False,
        primary_key = True,
        autoincrement=True
    )

    content_id = db.Column(
        db.Integer,
        db.ForeignKey('MentorContent.content_id')
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('CourseStudents.user_id')
    )

    upload_date = db.Column(
        db.Date,
        nullable=True
    )
    
    data = db.Column(
        db.LargeBinary,
        nullable=False
    )

    filename = db.Column(
        db.String(30),
        nullable = False
    )
    #grade_id = db.relationship('Grade')
    


class Grade(db.Model):  #submission
    __tablename__ = 'Grade'

    upload_id = db.Column(
        db.Integer,
        db.ForeignKey('MenteeAssignment.upload_id'),
        primary_key = True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('MenteeAssignment.user_id'),
        primary_key = True
    )

    score = db.Column(
        db.Integer,
        nullable=False
    )

    max_marks = db.Column(
        db.Integer,
        nullable=False
    )
class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('LoginDetails.user_id'), nullable = False)
	replies = db.relationship('Reply', backref = 'post', lazy = True)
	course_id=db.Column(db.Integer, db.ForeignKey('Course.course_id'), nullable = False)
	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"
    


class Reply(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('LoginDetails.user_id'), nullable = False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)
	def __repr__(self):
         return f"Reply('{self.content}')"
    