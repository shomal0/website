from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from .models import User

db = SQLAlchemy()
DB_NAME = "database.db"


def create_website():
    website = Flask(__name__)
    website.config['SECRET_KEY'] = 'shalom korim li shomal'
    website.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
   # website.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
    db.init_app(website)

    from .views import views
    from .auth import auth

    website.register_blueprint(views, url_prefix='/')
    website.register_blueprint(auth, url_prefix='/')

    

    with website.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(website)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return website

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))