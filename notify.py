from asyncio.windows_events import NULL
from urllib import response
import smtplib
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import time
import datetime
from datetime import date
from dateutil import parser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio


Session = sessionmaker()
session = Session()

class notify:

    db = SQLAlchemy()
    app = NULL
    def __init__(self, db, app):
        self.db= db
        self.app= app

    gmail_user = 'lmsdesis22@gmail.com'
    gmail_password = 'palak123'

    sent_from = gmail_user
    subject = 'Assignment Due'
    body = 'Hey Educatee, your Assignment is Due!!'
    

    def newsend(self, to):
        msg = MIMEMultipart()
        msg['From'] = 'lmsdesis22@gmail.com'
        msg['To'] = ", ".join(to)
        print(msg['To'])
        msg['Subject'] = 'Assignment Due'
        text = 'Hey Educatee, your Assignment is Due!!'
        part1 = MIMEText(text, 'plain')
        msg.attach(part1)
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(self.gmail_user, self.gmail_password)
            smtp_server.sendmail(self.sent_from, to, msg.as_string())
            smtp_server.close()
            print ("Email sent successfully!")
        except Exception as ex:
            print ("Something went wrong….",ex)

    def newsend2(self, to, courses, namec):

        for i in range(len(to)):
            msg = MIMEMultipart()
            msg['From'] = 'lmsdesis22@gmail.com'
            msg['To'] = to[i]
            #print(msg['To'])
            msg['Subject'] = 'Your ' + namec[i] + ' Due'
            text = 'Hey Educatee,\n\nYour Assignment (' + namec[i] + ') for ' + courses[i] + ' is Due!!\n'
            part1 = MIMEText(text, 'plain')
            msg.attach(part1)
            try:
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.ehlo()
                smtp_server.login(self.gmail_user, self.gmail_password)
                smtp_server.sendmail(self.sent_from, to[i], msg.as_string())
                smtp_server.close()
                print ("Email sent successfully!")
            except Exception as ex:
                print ("Something went wrong….", ex)



    def row2dict(self, row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))

        return d
    
    def getStudentsFromDB(self):
        response= []
        with self.app.app_context():
            rs= self.db.engine.execute("Select ContentTypes.content_name, MentorContent.due_date, Course.course_name, MentorContent.content_id, LoginDetails.email From MentorContent INNER JOIN Course ON Course.course_id = MentorContent.course_id INNER JOIN Course_Students ON Course.course_id = Course_Students.course_id INNER JOIN User ON Course_Students.student_id = User.user_id INNER JOIN LoginDetails ON User.user_id = LoginDetails.user_id INNER JOIN ContentTypes ON mentorcontent.content_id= ContentTypes.content_id")
            for row in rs:
                #print("palak")
                data= dict(row)
                response.append(data)
                #print(row)
        return response

    def filterstudents(self, Students):
        response= []
        for student in Students:
            #print(type(student["due_date"]))
            today = date.today()
            tomorrow = today + datetime.timedelta(days=1)
            fdate= str(student["due_date"] or "")
            if(fdate!= ""):
                due_date= parser.parse(fdate)
                #print(due_date.date())
                #print(tomorrow)
                if(tomorrow == due_date.date()):
                    #print("hi")
                    #print(student)
                    response.append(student)
        return response

    def SendMail(self, Students):
        emails= []
        courses= []
        namec= []
        for student in Students:
            emails.append(student["email"])
            print(student)
            courses.append(student["course_name"])
            namec.append(student["content_name"])
        emails.append("palakag1410@gmail.com")
        courses.append("physics")
        namec.append("assign1")
        self.newsend2(emails, courses, namec)
        
    
    def keepChecking(self):
        while 1:
            Students = self.getStudentsFromDB()
            FilteredStudents = self.filterstudents(Students)
            self.SendMail(Students)
            time.sleep(720*2*60)