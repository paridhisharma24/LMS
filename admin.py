from cmath import nan
from tracemalloc import start
import pandas as pd
import string
import random
from datetime import datetime
from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    url_for,
    request,
    render_template,
)
from sqlalchemy import null
from __init__ import db
from flask_login import current_user
from educatee import upload
from models import Course, CourseStudents, CourseInstance, User, LoginDetails
import xlsxwriter
import io
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint("admin", __name__)


@admin.route("/signUpUser", methods=["GET", "POST"])
def signUpUser():
    if request.method == "POST":
        file = request.files["file"]
        data = pd.read_excel(file).to_dict()

        failed = []

        for i in range(len(data["email"])):
            email = data["email"][i]
            password = data["password"][i]
            first_name = data["First Name"][i]
            last_name = data["Last Name"][i]
            # from a timestamp obeject to string(only the date part)
            dob_temp = str(data["dob"][i]).split()[0]
            if dob_temp == "nan":
                dob = None
            else:
                dob = datetime.strptime(dob_temp, "%Y-%m-%d")

            role = data["role"][i]
            salt = "".join(random.choices(string.ascii_uppercase + string.digits, k=20))
            user = LoginDetails.query.filter_by(email=email).first()
            if user:  # user with same email exists
                # flash('Email address already exists')
                print(user)
                failed.append({"seq_no": i, "name": (first_name + " " + last_name)})
                # return redirect(url_for('auth.signup'))
            else:
                new_login = LoginDetails(
                    email=email,
                    password=generate_password_hash(password + salt, method="sha256"),
                    salt=salt,
                    role=role,
                    first_name=first_name,
                    last_name=last_name,
                )
                new_user = User(dob=dob)
                # phone_no = PhoneNo( phone = request.form.get('phone_no'))
                # address = request.form.get('address')
                new_login.user.append(new_user)
                # new_user.phone_no.append(phone_no)
                print(new_login)
                db.session.add(new_login)
                db.session.commit()
        # flash('New Users added!!')

    return render_template("signup_confirmation.html", failed=failed)


@admin.route("/addCourse", methods=["GET", "POST"])
def addCourse():
    if request.method == "GET":
        return render_template("addCourse.html", name=current_user.first_name)
    else:
        print(request.form.get("courseName"))
        if request.form.get("courseName") == "":
            return render_template(
                "addCourse.html",
                name=current_user.first_name,
                message="Please Enter a Valid Course Name",
            )
        new_course = Course(course_name=request.form.get("courseName"))
        db.session.add(new_course)
        db.session.commit()
        return render_template(
            "addCourse.html",
            name=current_user.first_name,
            message="New Course Registered!!!",
        )


@admin.route("/getAllStudents", methods=["GET", "POST"])
def getAllStudents():
    # create excel sheet with all students(user_id, name, email)
    users = LoginDetails.query.filter_by(role=3)
    user_ids = []
    names = []
    emails = []
    for useri in users:
        user_ids.append(useri.user_id)
        names.append(useri.first_name + " " + useri.last_name)
        emails.append(useri.email)
    df = pd.DataFrame({"user_id": user_ids, "Name": names, "email": emails})
    buffer = io.BytesIO()
    df.to_excel(buffer, sheet_name="Sheet1", index=False)
    headers = {
        "Content-Disposition": "attachment; filename=students_list.xlsx",
        "Content-type": "application/vnd.ms-excel",
    }
    return Response(
        buffer.getvalue(), mimetype="application/vnd.ms-excel", headers=headers
    )


@admin.route("/addStudent", methods=["GET", "POST"])
def addStudent():
    if request.method == "GET":
        return render_template(
            "addStudent.html",
            name=current_user.first_name,
            courses=db.session.query(Course).all(),
        )
    else:
        course_id = request.form.get("courseId")
        # student_id = request.form.get('studentId')
        file = request.files["file"]
        data = pd.read_excel(file).to_dict()

        # return f'{course_id}'

        for uid in data["user_id"]:
            student_id = data["user_id"][uid]
            cs_object = CourseStudents.query.filter_by(
                course_id=course_id, student_id=student_id
            ).first()
            print(cs_object)
            # if student is already added do nothing
            if not cs_object:
                print("hey")
                new_courseStudent = CourseStudents(
                    course_id=course_id, student_id=student_id
                )
                db.session.add(new_courseStudent)
                db.session.commit()
        return render_template(
            "addStudent.html",
            name=current_user.first_name,
            message="New Students added!!",
        )
        pass
    pass


@admin.route("/addEducator", methods=["GET", "POST"])
def addEducator():
    if request.method == "GET":
        return render_template(
            "addEducator.html",
            name=current_user.first_name,
            courses=db.session.query(Course).all(),
            educators=LoginDetails.query.filter_by(role=2),
        )
    else:
        course_id = request.form.get("courseId")
        mentor_id = request.form.get("educatorId")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        upload_date = request.form.get("start_date")
        if start_date == "":
            start_date = None
        if end_date == "":
            end_date = None
        if upload_date == "":
            upload_date = None
        new_courseInstance = CourseInstance(
            course_id=course_id,
            mentor_id=mentor_id,
            start_date=start_date,
            end_date=end_date,
            upload_date=upload_date,
        )
        db.session.add(new_courseInstance)
        db.session.commit()
        return render_template(
            "addEducator.html",
            name=current_user.first_name,
            message="New Educator added!!",
        )
        pass
    pass
