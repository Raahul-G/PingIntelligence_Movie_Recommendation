from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'PLEASE BE NICE'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    create_database(app)
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():         # This is needed to provide context to where the database should
            db.create_all()             # be made
        print('Created Database!')