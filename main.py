####################################################################
###############          Import packages         ###################
####################################################################
from flask import session,Blueprint, render_template, flash
from flask_login import login_required, current_user
from datetime import timedelta
from __init__ import create_app, db


####################################################################
# our main blueprint
main = Blueprint('main', __name__)
####################################################################
# @main.before_request
# def before_request():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(minutes=.5)
#     session.modified = True

@main.route('/') 
def index():
    return render_template("index.html")

####################################################################
@main.route('/dashboard') 
@login_required
def dashboard():
    if current_user.role == 'Admin':
        return render_template('adminDashboard.html', name=(current_user.first_name+' '+current_user.last_name))
    elif current_user.role == 'Educatee':
        return render_template('dashboard_educatee.html', name=(current_user.first_name+' '+current_user.last_name))
    elif current_user.role == 'Educator':
        return render_template('dashboard_educator.html', name=(current_user.first_name+' '+current_user.last_name))


####################################################################
app = create_app() 
####################################################################
if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True) # run the flask app on debug mode
