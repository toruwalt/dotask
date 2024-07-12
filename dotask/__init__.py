#!/usr/bin/python3
"""My Taskkeeper"""

import os, enum, time

from flask import Flask
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message

login_manager = LoginManager()

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = "1234567890"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dotask.db')

"""
app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'toruwalt@gmail.com'
    #MAIL_PASSWORD = 'your_password'
))
"""


db = SQLAlchemy(app)
bcrypt = Bcrypt(app) 
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)

login_manager.login_view = "hello_login"

from dotask import routes
