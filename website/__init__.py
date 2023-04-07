from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"


def create_website():
    website = Flask(__name__)
    website.config['SECRET_KEY'] = 'shalom korim li shomal'
    website.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(website)

    from .views import views
    from .auth import auth

    website.register_blueprint(views, url_prefix='/')
    website.register_blueprint(auth, url_prefix='/')

    from .models import User

    with website.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(website)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return website


def create_database(website):
    if not path.exists('website/' + DB_NAME):
        db.create_all(website=website)
        print('created database')
