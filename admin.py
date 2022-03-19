import pandas as pd
from flask import Blueprint,redirect,url_for,request,render_template
from sqlalchemy import null
from __init__ import db
from flask_login import current_user
from models import Course, CourseStudents, CourseInstance

admin = Blueprint('admin',__name__)

@admin.route('/signUpUser',methods=['GET','POST'])
def signUpUser():
    if request.method == 'POST':
        file = request.files['file']
        data = pd.read_excel(file).to_dict()
        
        new_login = [data['Roll Number'][0],data['Name of Student'][0]]
        return f'Uploaded: {new_login}'
    return redirect(url_for('main.dashboard'))



@admin.route('/addCourse',methods=['GET','POST'])
def addCourse():
    if request.method == 'GET':
        return render_template('addCourse.html', name=current_user.first_name)
    else:
        print(request.form.get('courseName'))
        if(request.form.get('courseName') == ""):
            return render_template('addCourse.html', name=current_user.first_name,message="Please Enter a Valid Course Name")
        new_course = Course(
            course_name = request.form.get('courseName')
        )
        db.session.add(new_course)
        db.session.commit()
        return render_template('addCourse.html', name=current_user.first_name,message="New Course Registered!!!")


@admin.route('/addStudent',methods=['GET','POST'])
def addStudent():
    if request.method == 'GET':
        return render_template('addStudent.html', name=current_user.first_name)
    else:
        new_courseStudent = CourseStudents(
            course_id = request.form.get('courseId'),
            user_id = request.form.get('studentID')
        )
        db.session.add(new_courseStudent)
        db.session.commit()
        return render_template('addStudent.html', name=current_user.first_name,
        message="New Student added!!")
        pass
    pass


@admin.route('/addInstructor',methods=['GET','POST'])
def addInstructor():
    if request.method == 'GET':
        return render_template('addInstructor.html', name=current_user.first_name)
    else:
        new_courseStudent = CourseInstance(
            course_id = request.form.get('courseId'),
            user_id = request.form.get('studentID')
        )
        db.session.add(new_courseStudent)
        db.session.commit()
        return render_template('addInstructor.html', name=current_user.first_name,
        message="New Instructor added!!")
        pass
    pass