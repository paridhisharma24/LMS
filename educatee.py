from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import null
from werkzeug.security \
         import generate_password_hash, check_password_hash
from models import Course
from models import MenteeAssignment, CourseStudents
# from models import User
from flask_login import login_user, logout_user, \
                                     login_required, current_user
from __init__ import create_app, db

# our main blueprint
educatee = Blueprint('educatee', __name__)

@educatee.route('/upload', methods=['GET', 'POST']) 
def upload(): 
    if request.method == 'POST':
        file = request.files['file']

        # upload = MenteeAssignment(filename=file.filename, data=file.read())
        # db.session.add(upload)
        # db.session.commit()

        return f'Uploaded: {file.filename}'
    return redirect(url_for('main.dashboard'))

@educatee.route('/checkgrades', methods=['GET', 'POST']) 
def checkgrades(): 
    grades = CourseStudents.query.filter(CourseStudents.user_id == current_user.id ).all() # need to create grades database (roll no, couse name, couse grade)
    grade_text = '<ul>'
    for grade in grades:
        if(grade.course_grade==null):
            return "Grades are not given"
        grade_text += '<li>' + grade.course_name + ' -> ' + grade.course_grade + '</li>'
    if( grade_text == '<ul>'):
          return "Grades are not given"
    grade_text += '</ul>'
    return grade_text
   


# @educatee.route('/checkcourses', methods=['GET', 'POST']) 
# def checkcourses(): 
#     course_list= db.session.query(CourseStudents,Course).filter(CourseStudents.course_id==Course.course_id).all()
#     courses_text= '<ul>'
#     # for course in course_list:
#     #     if(course.student_id==current_user.id):
#     #      courses_text += '<li>' + course_list.course_id+ ' -> ' + course_list.course_name +'</li>'
#     # courses_text += '</ul>'
#     return courses_text
   
