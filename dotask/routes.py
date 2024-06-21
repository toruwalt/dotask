from flask import render_template,  redirect, request, url_for, flash
from dotask import app, db
from . import bcrypt
from dotask.forms import RegisterForm, LoginForm
from dotask.models import User
from dotask import login_manager, current_user, login_user, login_required, logout_user

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/dashboard")
@login_required
def hello_dashboard():
    """The Dashboard"""
    return render_template('dashboard.html', name=current_user.first_name)

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
            user = User.query.filter_by(email=form.email.data).first()
            username = User.query.filter_by(username=form.username.data).first()
            if user:
                flash("Email already used")
                return render_template('register.html')
            if username:
                flash("Username already exist")
                return render_template('register.html')
            user = User(
                email = form.email.data,
                username = form.username.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('hello_login'))
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
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('login.html', form=form)

    if request.method == 'POST':
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                password = user.password
                if bcrypt.check_password_hash(password, form.password.data) == True:
                    current_user.is_authenticated
                    login_user(user)

                    return redirect(url_for('hello_dashboard'))

                else:
                    flash("Invalid login credentials. Please check your password.", category='error')
                    return render_template('login.html')
            
            else:
                    flash("Invalid login credentials. Please check your email.", category='error')
                    return render_template('login.html')
        else:
            flash(form.errors, category='error')
            return render_template('login.html')
       

@app.route("/contact_us", methods=['GET', 'POST'])
@login_required
def hello_contact_us():
    """The about page"""
    return "<p>Hello, Contact Us!</p>"

@app.route("/profile")
@login_required
def hello_profile():
    """The profile page"""
    return render_template('profile.html')


@app.route("/tasks")
@login_required
def hello_tasks():
    return render_template("tasks.html")


@app.route("/settings")
@login_required
def hello_settings():
    return render_template("settings.html")

@app.route("/logout")
def hello_logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('hello_login'))