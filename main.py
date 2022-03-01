####################################################################
###############          Import packages         ###################
####################################################################
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from __init__ import create_app, db

####################################################################
# our main blueprint
main = Blueprint('main', __name__)
####################################################################
@main.route('/') # home page that return 'index'
def index():
    return render_template("index.html")

####################################################################
@main.route('/dashboard') # dashboard page that return 'dashboard'
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)

####################################################################
app = create_app() # we initialize our flask app using the            
                   #__init__.py function
####################################################################
if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True) # run the flask app on debug mode
