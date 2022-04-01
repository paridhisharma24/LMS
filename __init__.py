from sqlite3 import OperationalError
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from sqlalchemy import create_engine

db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    
    app.config['SECRET_KEY'] = 'secret-key-goes-here' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    
    
    # try:
    #     create_engine(app.config['SQLALCHEMY_DATABASE_URI']).connect()
    # except OperationalError:
    #     db.create_all()

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' 
    login_manager.init_app(app)
    from models import LoginDetails
    @login_manager.user_loader
    def load_user(user_id):
        return LoginDetails.query.get(int(user_id))
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    # blueprint for non-auth parts of app
    from educatee import educatee as educatee_blueprint
    app.register_blueprint(educatee_blueprint)

    from educator import educator as educator_blueprint
    app.register_blueprint(educator_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app