from cmath import nan
import pandas as pd
import string    
import random 
from datetime import datetime 
from flask import Blueprint, flash,redirect,url_for,request,render_template
from sqlalchemy import null
from __init__ import db
from flask_login import current_user
from models import Course, CourseStudents, CourseInstance, User, LoginDetails
from hashlib import new
from time import strptime
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint('admin',__name__)

@admin.route('/signUpUser',methods=['GET','POST'])
def signUpUser():
    if request.method == 'POST':
        file = request.files['file']
        data = pd.read_excel(file).to_dict()

        failed = []
        
        for i in range(len(data['email'])):
            email = data['email'][i]
            password = data['password'][i]
            first_name = data['First Name'][i]
            last_name = data['Last Name'][i]
            # from a timestamp obeject to string(only the date part)
            dob_temp = str(data['dob'][i]).split()[0]
            if dob_temp == 'nan':
                dob = None
            else:
                dob = datetime.strptime(dob_temp,'%Y-%m-%d')

            role = data['role'][i]
            salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))    
            user = LoginDetails.query.filter_by(email=email).first()
            if user: #user with same email exists
                # flash('Email address already exists')
                print(user)
                failed.append({'seq_no':i,'name':(first_name+' '+last_name)})
                # return redirect(url_for('auth.signup'))
            else:            
                new_login = LoginDetails(email=email,password=generate_password_hash(password+salt, method='sha256'), salt = salt, role = role,\
                                    first_name = first_name, last_name = last_name )
                new_user = User( dob = dob)
                # phone_no = PhoneNo( phone = request.form.get('phone_no'))
                # address = request.form.get('address')
                new_login.user.append(new_user)
                # new_user.phone_no.append(phone_no)
                print(new_login)
                db.session.add(new_login)
                db.session.commit()
        # flash('New Users added!!')
        
    return render_template('signup_confirmation.html',failed = failed)


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