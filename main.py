####################################################################
###############          Import packages         ###################
####################################################################
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from __init__ import create_app, db
from models import ContentTypes, UserRoles

####################################################################
# our main blueprint
main = Blueprint('main', __name__)
####################################################################
@main.route('/') 
def index():
    """new_role = UserRoles(role=1,role_name="Adminstration")
    db.session.add(new_role)
    new_role = UserRoles(role=2,role_name="Educator")
    db.session.add(new_role)
    new_role = UserRoles(role=3,role_name="Educatee")
    db.session.add(new_role)
    db.session.commit()

    content = ContentTypes(content_id=1, content_name="Assignment")
    db.session.add(content)
    content = ContentTypes(content_id=2,content_name="Notes")
    db.session.add(content)
    content = ContentTypes(content_id=3,content_name="Lecture")
    db.session.add(content)
    db.session.commit()"""
    
    return render_template("index.html")

####################################################################
@main.route('/dashboard') 
@login_required
def dashboard():
    if current_user.role == 1:
        return render_template('dashboard_admin.html', name=(current_user.first_name+' '+current_user.last_name))
    elif current_user.role == 3:
        return render_template('educatee.html', name=(current_user.first_name+' '+current_user.last_name))
    else:
        return render_template('dashboard.html', name=(current_user.first_name+' '+current_user.last_name))

    #return render_template('educator.html', name=current_user.first_name)
    #return render_template('educator.html', name=(current_user.first_name+' '+current_user.last_name), r=current_user.role, content=db.session.query(ContentTypes).all())

####################################################################
app = create_app() 
####################################################################
if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True) # run the flask app on debug mode
