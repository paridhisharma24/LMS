####################################################################
##############          Import packages      #######################
####################################################################
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security \
         import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, \
                                     login_required, current_user
from __init__ import db
import string    
import random # define the random module  


####################################################################
auth = Blueprint('auth', __name__) # create a Blueprint object that 
                                   # we name 'auth'

####################################################################
@auth.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method=='GET': 
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Please sign up first!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password+user.salt):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.dashboard'))
####################################################################
@auth.route('/signup', methods=['GET', 'POST'])

def signup(): 
    if request.method=='GET': 
        return render_template('signup.html')
    else: 
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role')
        salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))    
        user = User.query.filter_by(email=email).first()
        if user: #user with same email exists
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        
        new_user = User(email=email, name=name, \
                        password=generate_password_hash(password+salt, \
                        method='sha256'),\
                        role = role, salt = salt)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

###################################################################
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))