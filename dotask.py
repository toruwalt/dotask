#!/usr/bin/python3
"""My Taskkeeper"""

import os, enum
from flask import Flask, render_template,  redirect, request, url_for, flash
from forms import RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date
from sqlalchemy import Enum
from sqlalchemy.orm import relationship


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = "1234567890"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dotask.db')


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    tasks = relationship('Task', back_populates='user')

class TaskStatus(enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(Enum(TaskStatus))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='tasks')


with app.app_context():
    db.create_all()


@app.route("/dashboard")
def hello_dashboard():
    """The Dashboard"""
    return render_template('dashboard.html')


@app.route("/")
@app.route("/home")
def hello_home():
    """The homepage"""
    return render_template('landing_page.html')

@app.route("/company")
def hello_company():
    """The about page"""
    return "<p>Learn about the Company!</p>"

@app.route("/blog")
def hello_blog():
    """The about page"""
    return "<p>Hello, Blog!</p>"



@app.route("/register", methods=['GET', 'POST'])
def hello_register():
    form = RegisterForm(request.form)
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        if form.validate():
            user = User(
                email = form.email.data,
                username = form.username.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                password = form.password.data
                )
            db.session.add(user)
            db.session.commit()
            flash("Registration Succesful")
            return redirect(url_for('hello_dashboard'))
            
        else:
            flash(form.errors, category='error')
            return render_template('register.html')
    
@app.route("/submit", methods=['GET', 'POST'])
def hello_submit():
    """
    if request.method == "POST":
        username = request.form["username"]
        # Process the username here
        return f"Hello, {username}!"
    """
    return render_template("submit.html")

@app.route("/login", methods=['GET', 'POST'])
def hello_login():
    """
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))"""
    return render_template('login.html')

@app.route("/contact_us", methods=['GET', 'POST'])
def hello_contact_us():
    """The about page"""
    return "<p>Hello, Contact Us!</p>"

if __name__ == "__main__":
    app.run(debug=True)
