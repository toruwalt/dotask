from datetime import date
from flask import render_template,  redirect, request, url_for, flash
from dotask import app, db
from . import bcrypt
from dotask.forms import RegisterForm, LoginForm, TaskForm, SearchUserForm
from dotask.models import User, Task
from dotask import login_manager, current_user, login_user, login_required, logout_user

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/dashboard")
@login_required
def hello_dashboard():
    """The Dashboard"""
    try:
        tasks = current_user.tasks
        if tasks:
            return render_template("dashboard.html", tasks=tasks)
    except:
        return render_template("dashboard.html")

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
        return render_template('register.html')

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
            return render_template('login.html')
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
        return render_template('login.html')

    if request.method == 'POST':
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                password = user.password
                if bcrypt.check_password_hash(password, form.password.data) == True:
                    login_user(user)
                    return redirect(url_for('hello_dashboard', user=current_user))

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
    try:
        task_all = 0
        task_in = 0
        task_com = 0
        task_can = 0
        tasks = current_user.tasks
        if tasks:
            for task in tasks:
                task_all += 1
                if task.status.name == 'Cancelled':
                    task_can += 1
                elif task.status.name == 'Completed':
                    task_com += 1
                else:
                    task_in += 1
            return render_template('profile.html', current_user=current_user, task=task, task_all=task_all, task_in=task_in, task_com=task_com, task_can=task_can)
        else:
            return render_template('profile.html', current_user=current_user)
    except:
        return render_template('profile.html', current_user=current_user)

    
@app.route("/invites")
@login_required
def hello_invites():
     return render_template('invites.html')

@app.route("/search_user", methods=['GET','POST'])
@login_required
def hello_search_user():
    if request.method == 'GET':
        return render_template("invites_to_task.html")

    if request.method == 'POST':
        form = SearchUserForm(request.form)
        if form.validate():
            searched_user = User.query.filter_by(username=form.username.data).first()
            if searched_user == current_user:
                flash("You can't invite yourself")
                return render_template('invites_to_task.html')
            if searched_user:
                return render_template('invites_to_task.html', searched_user=searched_user)
            else:
                flash('User not found')
                return render_template('invites_to_task.html')
        else:
            flash('Enter a username')
            return render_template('invites_to_task.html')

@app.route("/invite_to_task/<task_id>", methods=['GET','POST'])
@login_required
def hello_invite_to_task(task_id):
    try:
        task = db.session.query(Task).get(task_id)
        return render_template('invites_to_task.html', task=task)
    except:
        flash("Sorry, couldn't query the database")
        return redirect(url_for('hello_each_task', task_id=task_id))



@app.route("/tasks")
@login_required
def hello_tasks():
    try:
        tasks = current_user.tasks
        """
        To get the Invited tasks, do
        1- tasks = Task.query.filter_by(shared_id=current_user.id).all()
        2- Render the template, but passed the shared_task as well owned_task
            i.e return render_template("tasks.html", tasks=tasks, shared_tasks=shared_tasks)

        This goes for cancelled, completed and in progress.
        """
        if tasks:
            return render_template("tasks.html", tasks=tasks)
        else:
            return render_template("tasks.html")
    except:
        return render_template("tasks.html")

    
@app.route("/in_process_tasks")
@login_required
def hello_in_process_tasks():
    try:
        tasks = current_user.tasks
        if tasks:
            return render_template("in_process_tasks.html", tasks=tasks)
        else:
            return render_template("in_process_tasks.html")
    except:
        return render_template("in_process_tasks.html")

    
@app.route("/completed_tasks")
@login_required
def hello_completed_tasks():
    try:
        tasks = current_user.tasks
        if tasks:
            return render_template("completed_tasks.html", tasks=tasks)
        else:
            return render_template("completed_tasks.html")
    except:
        return render_template("completed_tasks.html")    
    
@app.route("/cancelled_tasks")
@login_required
def hello_cancelled_tasks():
    try:
        tasks = current_user.tasks
        if tasks:
            return render_template("cancelled_tasks.html", tasks=tasks)
        else:
            return render_template("cancelled_tasks.html")
    except:
        return render_template("cancelled_tasks.html")

@app.route("/new_task", methods=['GET', 'POST'])
def hello_new_task():
    user = current_user
    if request.method == 'GET':
        return render_template("new_task.html")

    if request.method == 'POST':
        form = TaskForm(request.form)
        if form.validate():
            try:
                due_date_str = form.due_date.data
                """year, month, day = map(int, due_date_str.split('-')[:3])
                due_date = date(year, month, day)"""
                task = Task(
                    title  = form.title.data,
                    description  = form.description.data,
                    due_date = due_date_str,
                    #due_date = due_date,
                    status = "In_Progress",
                    tag = form.tag.data
                )
                user.assigned_tasks.append(task)
                db.session.commit()
                
                flash('Task created successfully!')
                task_id = task.id
                return redirect(url_for('hello_each_task',task_id=task_id))  # Replace with your desired route

            except Exception as e:
                flash(f'Error creating task: {str(e)}')
                return render_template("new_task.html")
        else:
            flash(form.errors, category='error')
            return render_template('new_task.html')

@app.route("/task/<task_id>", methods=['GET','POST'])
@login_required
def hello_each_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task:
            return render_template("each_task.html", task=task)

@app.route("/edit/<task_id>", methods=['GET','POST'])
@login_required
def hello_edit_task(task_id):
        task = Task.query.get_or_404(task_id)
        if task:
            return render_template("edit_task.html", task=task)
        
@app.route("/save_task/<task_id>", methods=['GET','POST'])
@login_required
def hello_save_task(task_id):
        form = TaskForm(request.form)
        task = Task.query.get_or_404(task_id)
        if form.validate():
            due_date_str = form.due_date.data
            form = request.form
            due_date_str = form.get('due_date')
            year, month, day = map(int, due_date_str.split('-')[:3])
            due_date = date(year, month, day)
            task = Task.query.get_or_404(task_id)
            try:
                if task:
                    task.title  = form.get('title')
                    task.description  = form.get('description')
                    task.due_date = due_date
                    task.status = form.get('status')
                    task.tag = form.get('tag')
                    task.verified = True
                    db.session.commit()
                    flash('Task updated successfully!')
                    task_id = task.id
                    return redirect(url_for('hello_each_task',task_id=task_id))
            except Exception as e:  # Catch potential errors during data processing
                flash(f'Error saving task: {str(e)}')
                return render_template("each_task.html", task=task)
        else:
            flash(form.errors, category='error')
            return render_template('edit_task.html', task=task)
        
@app.route("/delete/<task_id>", methods=['GET','POST'])
@login_required
def hello_delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        user = current_user
        if task:
            user.assigned_tasks.remove(task)
            db.session.commit()
            flash("Task Deleted")
            return redirect(url_for('hello_dashboard'))  # Correct with quotes

        

@app.route("/settings")
@login_required
def hello_settings():
    return render_template("settings.html")

@app.route("/logout")
def hello_logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('hello_login'))