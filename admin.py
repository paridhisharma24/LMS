from email import message
from flask import Blueprint,redirect,url_for,request,render_template
from sqlalchemy import null
from __init__ import db
from flask_login import current_user
from db_model import course_details, course_students, course_mentors

admin = Blueprint('admin',__name__)

@admin.route('/addCourse',methods=['GET','POST'])
def addCourse():
    if request.method == 'GET':
        return render_template('addCourse.html', name=current_user.name)
    else:
        print(request.form.get('courseName'))
        if(request.form.get('courseName') == ""):
            return render_template('addCourse.html', name=current_user.name,message="Please Enter a Valid Course Name")
        new_course = course_details(
            course_name = request.form.get('courseName')
        )
        db.session.add(new_course)
        db.session.commit()
        return render_template('addCourse.html', name=current_user.name,message="New Course Registered!!!")


@admin.route('/addStudent',methods=['GET','POST'])
def addStudent():
    if request.method == 'GET':
        return render_template('addStudent.html', name=current_user.name)
    else:
        new_courseStudent = course_students(
            course_id = request.form.get('courseId'),
            user_id = request.form.get('studentID')
        )
        db.session.add(new_courseStudent)
        db.session.commit()
        return render_template('addStudent.html', name=current_user.name,
        message="New Student added!!")
        pass
    pass


@admin.route('/addInstructor',methods=['GET','POST'])
def addInstructor():
    if request.method == 'GET':
        return render_template('addInstructor.html', name=current_user.name)
    else:
        new_courseStudent = course_mentors(
            course_id = request.form.get('courseId'),
            user_id = request.form.get('studentID')
        )
        db.session.add(new_courseStudent)
        db.session.commit()
        return render_template('addInstructor.html', name=current_user.name,
        message="New Instructor added!!")
        pass
    pass