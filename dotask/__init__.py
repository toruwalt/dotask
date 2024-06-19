#!/usr/bin/python3
"""My Taskkeeper"""

import os, enum, time

from flask import Flask
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = "1234567890"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dotask.db')


db = SQLAlchemy(app)
bcrypt = Bcrypt(app) 
migrate = Migrate(app, db)


from dotask import routes