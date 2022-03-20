from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import null
from models import User, MentorContent, CourseStudents, CourseInstance, Course, ContentTypes, Grade

from flask_login import current_user
from __init__ import db
from datetime import date
import pandas as pd
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
session = Session()

educator = Blueprint('educator', __name__)

@educator.route('/addContent', methods=['GET', 'POST']) 
def addContent(): 
    if request.method == 'GET':
        courses = Course.query.filter(CourseInstance.mentor_id == current_user.user_id ).all()
        return render_template('addContent.html', 
                                name=(current_user.first_name+' '+current_user.last_name),
                                content=db.session.query(ContentTypes).all(),
                                course=courses)

    else:
        file = request.files['file']
        course_id = request.form.get("course_id")
        due = request.form.get("due_date")
        upload_date = date.today()
        content = MentorContent(mentor_id=current_user.user_id,
                            data=file.read(),
                            course_id=course_id,
                            due_date=due,
                            upload_date=upload_date
                        )
        
        db.session.add(content)
        db.session.commit()

        flash( f'Uploaded: {file.filename}')
        return render_template('educator.html')



@educator.route('/addGrades', methods=['GET', 'POST']) 
def addGrades(): 
    if request.method == 'GET':
        return render_template('addGrades.html')

    else:
        file = request.files['file']
        file = pd.read_excel(file).to_dict()

        if(len(file) > 0):
            for i in range(len(file)):
                new_grade = Grade(id=file['assignment_id'][i],
                            user_id=file['user_id'][i],
                            score=file['score'][i],
                            max_marks=file['max_marks'][i]
                        )
                db.session.add(new_grade)
                db.session.commit()

        return render_template('educator.html')



@educator.route('/checkcourses', methods=['GET', 'POST']) 
def checkcourses(): 
    course_list= db.session.query(CourseInstance,Course).filter(CourseInstance.mentor_id==current_user.user_id ).all()
    for r in course_list:
        print(r.CourseInstance.instance_id,r.Course.course_name)

    return render_template('checkcourse.html', course_list=course_list)


@educator.route('/viewCourse', methods=['GET', 'POST']) 
def viewCourse():
    keys=request.args.get('course_id')
    return f'{keys}'
    render_template('coursepage.html')


