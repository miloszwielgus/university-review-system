from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager 
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS

db = SQLAlchemy()
DB_NAME = "unidatabase.db"


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = '3489qwako23i3nnASp'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['CORS_HEADERS'] = 'Content-Type'
    db.init_app(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User,Rating,Course,University

    create_database(app)

    login_manager=LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    admin = Admin(app) 
    admin.add_view(ModelView(User,db.session))
    admin.add_view(ModelView(University,db.session))
    admin.add_view(ModelView(Course,db.session))
    admin.add_view(ModelView(Rating,db.session))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
