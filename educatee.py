####################################################################
###############          Import packages         ###################
####################################################################
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import null
from werkzeug.security \
         import generate_password_hash, check_password_hash
from models import Course, Post, Reply
from models import Upload, Course_Students
from models import User
from flask_login import login_user, logout_user, \
                                     login_required, current_user
from __init__ import create_app, db
from forms import ReplyForm
####################################################################
# our main blueprint
educatee = Blueprint('educatee', __name__)

@educatee.route('/upload', methods=['GET', 'POST']) 
def upload(): 
    if request.method == 'POST':
        file = request.files['file']

        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded: {file.filename}'
    return redirect(url_for('main.dashboard'))

####################################################################
@educatee.route('/checkgrades', methods=['GET', 'POST']) 
def checkgrades(): 
    grades = Course_Students.query.filter(Course_Students.user_id == current_user.id ).all() # need to create grades database (roll no, couse name, couse grade)
    grade_text = '<ul>'
    for grade in grades:
        if(grade.course_grade==null):
            return "Grades are not given"
        grade_text += '<li>' + grade.course_name + ' -> ' + grade.course_grade + '</li>'
    if( grade_text == '<ul>'):
          return "Grades are not given"
    grade_text += '</ul>'
    return grade_text
   


####################################################################
@educatee.route('/checkcourses', methods=['GET', 'POST']) 
def checkcourses(): 
    course_list= db.session.query(Course_Students,Course).filter(Course_Students.course_id==Course.course_id).all()
    courses_text= '<ul>'
    for course in course_list:
        if(course.user_id==current_user.id):
         courses_text += '<li>' + course_list.course_id+ ' -> ' + course_list.course_name +'</li>'
    courses_text += '</ul>'
    return courses_text



   
	