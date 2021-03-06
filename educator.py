import base64
from fileinput import filename
from time import strptime
from flask import (
    Response,
    Blueprint,
    make_response,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)
from sqlalchemy import null
from models import (
    MentorContent,
    CourseStudents,
    CourseInstance,
    Course,
    ContentTypes,
    Grade,
    LoginDetails,
    MenteeAssignment
)
import io
from flask_login import current_user
from __init__ import db
from datetime import datetime, date
import pandas as pd
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
session = Session()

educator = Blueprint("educator", __name__)


@educator.route("/addContent", methods=["GET", "POST"])
def addContent():
    course_id = int(request.args.get("course_id"))
    if request.method == "GET":
        return render_template(
            "addContent.html",
            name=(current_user.first_name + " " + current_user.last_name),
            content=db.session.query(ContentTypes).all(),
            course_id=course_id,
        )

    else:
        file = request.files["file"]
        due = request.form.get("due_date")
        if due == "":
            due_date = None
        else:
            due_date = datetime.strptime(due, "%Y-%m-%d")
        upload_date = date.today()
        type = request.form.get("content_id")
        content = MentorContent(
            user_id=current_user.user_id,
            data=file.read(),
            course_id=course_id,
            due_date=due_date,
            upload_date=upload_date,
            type=type,
            filename=file.filename
        )

        db.session.add(content)
        db.session.commit()

        flash(f"Uploaded: {file.filename}")
        return redirect(url_for("educator.viewCourse", course_id=course_id))


@educator.route("/addGrades", methods=["GET", "POST"])
def addGrades():
    if request.method == "GET":
        course_id = request.form.get("course_id")
        assignment_id = request.form.get("assignment_id")
        return render_template("addGrades.html", course_id=course_id, assignment_id=assignment_id)

    else:
        file = request.files["file"]
        file = pd.read_excel(file).to_dict()

        if len(file) > 0:
            for i in range(len(file)):
                new_grade = Grade(
                    id=file["assignment_id"][i],
                    user_id=file["user_id"][i],
                    score=file["score"][i],
                    max_marks=file["max_marks"][i],
                )
                db.session.add(new_grade)
                db.session.commit()

        return redirect(url_for("main.dashboard"))


@educator.route("/viewCourse", methods=["GET", "POST"])
def viewCourse():
    course_id = int(request.args.get("course_id"))
    assignments = MentorContent.query.filter_by(course_id=course_id, content_id=1)
    notes = MentorContent.query.filter_by(course_id=course_id, content_id=2)
    lectures = MentorContent.query.filter_by(course_id=course_id, content_id=3)

    return render_template(
        "viewcourse_educator.html",
        course_id=course_id,
        course_name=Course.query.filter(Course.course_id == course_id)
        .first()
        .course_name,
        assignments=assignments,
        lectures=lectures,
        notes=notes,
    )


@educator.route("/viewContent")
def viewContent():
    content_id = request.args.get("content_id")
    filename = request.args.get("filename")
    return render_template("view_pdf.html", content_id=content_id, filename=filename)


@educator.route("/viewPdf/<content_id>")
def viewPdf(content_id=None):
    # return f'{content_id}'
    pdf = db.session.query(MentorContent).filter(MentorContent.content_id == content_id).first().data
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=%s.pdf" % "yourfilename"
    return response
    

@educator.route('/getAllStudents',methods=['GET','POST'])
def getAllStudents():
    #create excel sheet with all students(user_id, name, email)
    course_id = int(request.args.get('course_id'))
    course = db.session.query(Course).filter(course_id==course_id).all()

    assignment_id = int(request.args.get('content_id'))

    course_students = db.session.query(CourseStudents).filter(CourseStudents.course_id == course_id)
    users = db.session.query(LoginDetails, course_students).filter(LoginDetails.user_id == course_students.user_id).all()

    user_ids = []
    names = []
    emails = []
    upload = []

    for useri in users:
        user_ids.append(useri.user_id)
        names.append(useri.first_name + ' ' + useri.last_name)
        emails.append(useri.email)
        upload.append(useri.upload_id)

    df = pd.DataFrame(columns={'Course', 'upload_id', 'user_id', 'Name', 'email'})
    df['Course'] = course
    df['upload_id'] = upload
    df['user_id'] = user_ids
    df['Name'] = names
    df['email'] = emails

    #{'course': courses, 'assignment_id': assignment_id, 'user_id':user_ids, 'Name': names,  'email'}
    buffer = io.BytesIO()
    df.to_excel(buffer, sheet_name='Sheet1', index=False)
    headers = {
    'Content-Disposition': 'attachment; filename=students_list.xlsx',
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)
    

"""@educator.route('/getAssignment',methods=['GET','POST'])
def getAssignment():"""