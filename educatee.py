from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from models import Course
from models import MenteeAssignment, CourseStudents, MentorContent, Course
from datetime import datetime, date

# from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import create_app, db

# our main blueprint
educatee = Blueprint("educatee", __name__)


@educatee.route("/upload", methods=["GET", "POST"])
def upload():
    #assignment = int(request.args.get("assignment_id"))
    
    if request.method == "GET":
        return render_template("uploadAssignment.html")

    elif request.method == "POST":
        file = request.files["file"]
        
        upload = MenteeAssignment(assignment_id = 1, 
                                filename=current_user.first_name + "_assignment", 
                                user_id = current_user.user_id, 
                                data=file.read(),
                                upload_date = date.today()
                                )

        db.session.add(upload)
        db.session.commit()

        flash( f"Uploaded: {file.filename}")
        return redirect(url_for("main.dashboard"))


@educatee.route("/checkgrades", methods=["GET", "POST"])
def checkgrades():
    grades = CourseStudents.query.filter(
        CourseStudents.student_id == current_user.user_id).all()
    grade_text = "<ul>"
    for grade in grades:
        if grade.grade == null:
            return "Grades are not given"
        else:
            grade_text += "<li>" + grade.course_id + " -> " + grade.grade + "</li>"
    if grade_text == "<ul>":
        return "Grades are not given"
    grade_text += "</ul>"
    return grade_text


@educatee.route("/viewCourseEd", methods=["GET", "POST"])
def viewCourseEd():
    course_id = int(request.args.get("course_id"))
    assignments = MentorContent.query.filter_by(course_id=course_id, content_id=1)
    notes = MentorContent.query.filter_by(course_id=course_id, content_id=2)
    lectures = MentorContent.query.filter_by(course_id=course_id, content_id=3)

    return render_template(
        "viewcourse_educatee.html",
        course_name=Course.query.filter(Course.course_id == course_id)
        .first()
        .course_name,
        assignments=assignments,
        lectures=lectures,
        notes=notes,
    )
