from flask import session, Blueprint, render_template, flash
from flask_login import login_required, current_user
from datetime import timedelta
from __init__ import create_app, db
from models import UserRoles, ContentTypes, LoginDetails, CourseInstance, Course, CourseStudents
from notify import notify
import asyncio
import threading
from threading import Thread
import os



# our main blueprint
main = Blueprint("main", __name__)
# @main.before_request
# def before_request():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(minutes=.5)
#     session.modified = True

def runapp(app):
    #print("heyy")
    if __name__ == '__main__':
        db.create_all(app=create_app())
        app.run(debug=True) #run the flask app on debug mode
        #print("palak")


@main.route('/') 
def index():
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    print(current_user)

    if current_user.role == 1:
        return render_template(
            "dashboard_admin.html",
            name=(current_user.first_name + " " + current_user.last_name)
        )
    elif current_user.role == 3:
        student_course = (
            db.session.query(CourseStudents, Course)
            .filter(
                CourseStudents.user_id == current_user.user_id,
                CourseStudents.course_id == Course.course_id
            )
            .all()
        )
        return render_template(
            "dashboard_educatee.html",
            name=(current_user.first_name + " " + current_user.last_name),
            student_course=student_course
        )
    else:
        mentor_course = (
            db.session.query(CourseInstance, Course)
            .filter(
                CourseInstance.user_id == current_user.user_id,
                CourseInstance.course_id == Course.course_id
            )
            .all()
        )
        return render_template(
            "dashboard_educator.html",
            name=(current_user.first_name + " " + current_user.last_name),
            mentor_course=mentor_course
        )



app = create_app()

notifyy= notify(db, app)
# loop = asyncio.get_event_loop()
# loop.run_in_executor(None, notifyy.keepChecking)
if os.environ.get("firstrun")!= "1":
    threading.Thread(target= lambda: notifyy.keepChecking()).start()
    os.environ["firstrun"] = "1"

runapp(app)

