from flask import Flask
from __init__ import db
from flask_login import UserMixin
from datetime import datetime



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


#user specific details
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
        db.ForeignKey('UserRoles.role'),
        nullable = False
    )

    salt = db.Column(
        db.String(20),
        nullable=False
    )
   
    student = db.relationship('Course_Students')
    mentor = db.relationship('Course_Mentors')
    posts = db.relationship('Post', backref = 'author', lazy = True)
    replies = db.relationship('Reply', backref = 'user', lazy = True)


# Available Courses
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


#types of content like Assignments, notes, lecture, etc.
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


#contents of a course
#link is drive link where the assignment is uploaded
class Contents(UserMixin,db.Model):
    __tablename__ = 'Contents'
    date_of_upload = db.Column(
        db.Date,
        nullable=True
    )

    content_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement=True
    )

    course_id = db.Column(
        db.String(20),
        db.ForeignKey('Course.course_id')
    )
    
    content_type = db.Column(
        db.String(20),
        db.ForeignKey('ContentTypes.content_id')
    )

    link = db.Column(
        db.String(150),
        nullable=False
    )
    assignment = db.relationship('Assignment')


#student and course mapping
class Course_Students(UserMixin,db.Model):
    __tablename__ = 'Course_Students'

    course_id = db.Column(
        db.String(20),
        db.ForeignKey('Course.course_id'),
        primary_key = True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id'),
        primary_key = True
    )
    grade = db.Column(
        db.String(10),
        nullable=True
    )


#students and mentor mapping
class Course_Mentors(db.Model):
    __tablename__ = 'Course_Mentors'

    course_id = db.Column(
        db.String(20),
        db.ForeignKey('Course.course_id'),
        primary_key = True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id'),
        primary_key = True
    )


#details of assignment uploaded by students/mentees
class Assignment(db.Model):
    __tablename__ = 'Assignment'

    assignment_id = db.Column(
        db.String(20),
        db.ForeignKey('Contents.content_id'),
        primary_key = True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.user_id'),
    )

    link = db.Column(
        db.String(150),
        nullable=False
    )
class Upload(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    course_id=db.Column(db.String)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
	replies = db.relationship('Reply', backref = 'post', lazy = True)
	
	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"
    


class Reply(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)
	def __repr__(self):
         return f"Reply('{self.content}')"