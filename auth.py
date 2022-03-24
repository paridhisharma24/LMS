from hashlib import new
from time import strptime
from flask import Blueprint, render_template, redirect, session, url_for, request, flash
from numpy import append
from werkzeug.security \
         import generate_password_hash, check_password_hash
from models import User, UserRoles, LoginDetails, PhoneNo, Address, CourseInstance, Course, CourseStudents
from flask_login import login_user, logout_user, \
                                     login_required, current_user
from __init__ import db
import string    
import random 
from datetime import datetime 

auth = Blueprint('auth', __name__) 

auth = Blueprint('auth', __name__) 


@auth.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method=='GET': 
        if session.get('user'):
            login_user(session['user'])
            if current_user.role == 1:
                return render_template('dashboard_admin.html', name=(current_user.first_name+' '+current_user.last_name))
            elif current_user.role == 3:
                student_course = db.session.query(CourseStudents,Course).filter(CourseStudents.student_id==current_user.user_id, CourseStudents.course_id==Course.course_id ).all()
                return render_template('dashboard_educatee.html', name=(current_user.first_name+' '+current_user.last_name), student_course = student_course)
            else:
                mentor_course= db.session.query(CourseInstance,Course).filter(CourseInstance.mentor_id==current_user.user_id, CourseInstance.course_id==Course.course_id ).all()
                return render_template('dashboard_educator.html', name=(current_user.first_name+' '+current_user.last_name), mentor_course = mentor_course)


        else:
            return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = LoginDetails.query.filter_by(email=email).first()
        if not user:
            flash('Please sign up first!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password+user.salt):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        session['user'] = user
        login_user(user, remember=remember)
        return redirect(url_for('main.dashboard'))

@auth.route('/signup', methods=['GET', 'POST'])

def signup(): 
    if request.method=='GET':
        return render_template('signup.html',roles=db.session.query(UserRoles).all())
    else: 
        email = request.form.get('email')
        password = request.form.get('password')
        first_name  = request.form.get('first_name')
        last_name  = request.form.get('last_name')

        dob_temp = request.form.get('dob')
        if dob_temp == '':
           dob = None
        else:
           dob = datetime.strptime(dob_temp,'%Y-%m-%d')

        role = request.form.get('role')
        salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))    
        user = LoginDetails.query.filter_by(email=email).first()
        if user: #user with same email exists
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        
        new_login = LoginDetails(email=email,password=generate_password_hash(password+salt, method='sha256'), salt = salt, role = role,\
                                first_name = first_name, last_name = last_name )

        new_user = User( dob = dob)
        phone_no = PhoneNo( phone = request.form.get('phone_no'))
        # address = request.form.get('address')
        
        new_login.user.append(new_user)
        new_user.phone_no.append(phone_no)
        db.session.add(new_login)
        db.session.commit()
        flash('You are sucess fully registered! Login now')
        return redirect(url_for('auth.login'))
        # return redirect(url_for('auth.login'), flash('You are sucess fully registered! Login now'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session[current_user] = None
    return redirect(url_for('main.index'))