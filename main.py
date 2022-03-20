from flask import session,Blueprint, render_template, flash
from flask_login import login_required, current_user
from datetime import timedelta
from __init__ import create_app, db
from models import UserRoles, ContentTypes, CourseInstance, Course, CourseStudents


# our main blueprint
main = Blueprint('main', __name__)
# @main.before_request
# def before_request():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(minutes=.5)
#     session.modified = True

@main.route('/') 
def index():
    # new_role = UserRoles(role=1,role_name="Adminstration")
    # db.session.add(new_role)
    # new_role = UserRoles(role=2,role_name="Educator")
    # db.session.add(new_role)
    # new_role = UserRoles(role=3,role_name="Educatee")
    # db.session.add(new_role)
    # db.session.commit()
    # content = ContentTypes(content_id=1, content_name="Assignment")
    # db.session.add(content)
    # content = ContentTypes(content_id=2,content_name="Notes")
    # db.session.add(content)
    # content = ContentTypes(content_id=3,content_name="Lecture")
    # db.session.add(content)
    # db.session.commit()
    
    return render_template("index.html")

####################################################################
@main.route('/dashboard') 
@login_required
def dashboard():
    print(current_user)
    
    if current_user.role == 1:
        return render_template('dashboard_admin.html', name=(current_user.first_name+' '+current_user.last_name))
    elif current_user.role == 3:
        student_course = db.session.query(CourseStudents,Course).filter(CourseStudents.student_id==current_user.user_id, CourseStudents.course_id==Course.course_id ).all()
        return render_template('dashboard_educatee.html', name=(current_user.first_name+' '+current_user.last_name), student_course = student_course)
    else:
        mentor_course= db.session.query(CourseInstance,Course).filter(CourseInstance.mentor_id==current_user.user_id, CourseInstance.course_id==Course.course_id ).all()
        return render_template('dashboard_educator.html', name=(current_user.first_name+' '+current_user.last_name), mentor_course = mentor_course)

    #return render_template('educator.html', name=current_user.first_name)
    #return render_template('educator.html', name=(current_user.first_name+' '+current_user.last_name), r=current_user.role, content=db.session.query(ContentTypes).all())


app = create_app() 
if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True) # run the flask app on debug mode
