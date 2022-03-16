from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
  
    db.init_app(app) 
    
    login_manager = LoginManager() 
    login_manager.login_view = 'auth.login' 
    login_manager.init_app(app)
    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app