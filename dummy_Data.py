from tkinter import INSERT
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
session = Session()

class dummyData:
    db = SQLAlchemy()
    app = None
    def __init__(self, db, app):
        self.db= db
        self.app= app
        self.addDataToUserRoles()

    def addDataToUserRoles(self):
        self.db.engine.execute('INSERT INTO UserRoles (role, role_name) VALUES(1, \'Admin\')')
        self.db.engine.execute('INSERT INTO UserRoles (role, role_name) VALUES(2, \'Mentor\')')
        print("random")
        self.db.engine.execute('INSERT INTO UserRoles (role, role_name) VALUES(3, \'Mentee\')')

    

    
