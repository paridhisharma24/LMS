####################################################################
###############          Import packages         ###################
####################################################################
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security \
         import generate_password_hash, check_password_hash
from db_model import Upload, course_students
from models import User
from flask_login import login_user, logout_user, \
                                     login_required, current_user
from __init__ import create_app, db

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
    grades = grades.query.filter_by(roll=current_user.user_id).all() # need to create grades database (roll no, couse name, couse grade)
    grade_text = '<ul>'
    for grade in grades:
        grade_text += '<li>' + grade.couse_name + ' -> ' + grade.course_grade + '</li>'
    grade_text += '</ul>'
    return grade_text
    return 'sql to db'


####################################################################
@educatee.route('/checkcourses', methods=['GET', 'POST']) 
def checkcourses(): 
    student_courses = course_students.query.filter_by(roll=current_user.user_id).all() #  course_students database 
    grade_text = '<ul>'
    for grade in grades:
        grade_text += '<li>' + grade.couse_name + ' -> ' + grade.course_grade + '</li>'
    grade_text += '</ul>'
    return grade_text
    return 'sql to courses'
