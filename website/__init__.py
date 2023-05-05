from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_website():
    website = Flask(__name__)
    website.config['SECRET_KEY'] = 'shalom korim li shomal'
    website.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    website.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    def load_user(user_id):
        return User.query.get(int(user_id))

    return website
