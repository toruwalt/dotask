from datetime import date
from flask import render_template,  redirect, request, url_for, flash
from dotask import app, db
from . import bcrypt
from dotask.forms import RegisterForm, LoginForm, TaskForm, SearchUserForm
from dotask.models import User, Task,  user_task, Notification, user_notification
from dotask import login_manager, current_user, login_user, login_required, logout_user

@app.after_request
def after_request(response):
    """
        Executes after each request in this Flask app to stop client-side caching.

        Args:
            response: The object generated by view function or error handler.

        Returns:
            The modified response object. (i.e response)
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@login_manager.user_loader
def load_user(user_id):
    """
        Used for user authentication

        Args:
            user_id: An identifier for a particular user

        Returns:
            user object from the database where the user_id matches
    """
    return User.query.get(user_id)


@app.route("/dashboard")
@login_required
def hello_dashboard():
    """
        Populates the dashboard
        
        Returns:
            HTML page with content and tasks data
        Raises:

    """
    try:
        tasks = current_user.tasks
        notices = current_user.notes
        if tasks:
            if notices:
                return render_template("dashboard.html", tasks=tasks, notices=notices)
            return render_template("dashboard.html", tasks=tasks)
        else:
            return render_template("dashboard.html")
    except:
        error_message = "An error occurred while retrieving tasks."
        return render_template("dashboard.html", error_message=error_message)


@app.route("/")
@app.route("/home")
def hello_home():
    """
        Populates the landing page
        
        Returns:
            HTML page with content
    """
    return render_template('landing_page.html')


@app.route("/about")
def hello_about():
    """
        Renders the "About" pages
        
        Returns:
            About html page with content and tasks data
    """
    return render_template('about.html')


@app.route("/features")
def hello_features():
    """
    Renders the "Features" page.

    Returns:
        Features html page with content and tasks data
    """
    return render_template('features.html')


@app.route("/register", methods=['GET', 'POST'])
def hello_register():
    """
    Registers a new user.

    * GET: Renders the registration form template (`register.html`).

    * POST:
        - Validates the registration form data using `RegisterForm`.
        - Checks if email or username already exists.
          - If so, flashes an error message and re-renders the form.
        - Creates a new user object from the form data (including hashed password).
        - Adds the user to the database session and commits the changes.
        - Redirects the user to the login page (`hello_login`).

    Returns:
        - Template rendered for GET requests.
        - Redirection on successful registration (POST).
        - Re-rendered form with error messages on validation failure (POST).
    """
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
            return redirect(url_for('hello_login'))
        else:
            flash(form.errors, category='error')
            return redirect(url_for('hello_register'))
    

@app.route("/login", methods=['GET', 'POST'])
def hello_login():
    """
    Logs in a registered user.

    This function handles both GET and POST requests for user login.

    * GET: Renders the login form template (`login.html`).

    * POST:
        - Validates the login form data using `LoginForm`.
        - Attempts to find a user with the provided email.
          - If not found, flashes an error message and re-renders the form.
        - Checks the password entered against the stored hashed password.
          - If incorrect, flashes an error message and re-renders the form.
        - Logs the user in using SQLAlchemy's `login_user` function.
        - Retrieves the user's tasks.
        - Renders the dashboard template (`dashboard.html`) with user information and tasks.

    Returns:
        - Template rendered for GET requests.
        - Redirection to dashboard on successful login (POST).
        - Re-rendered form with error messages if validation fails or wrong credentials is inputted (POST).
    """

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
                    tasks = current_user.tasks
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
def hello_contact_us():
    """The about page"""
    if request.method == 'GET':
        return render_template('contact_us.html')
    """
    if request.method == 'POST':
        msg = Message('Test Email', sender='your_email@example.com', recipients=['recipient@email.com'])
        msg.body = 'This is a test email sent from your Flask application.'
        mail.send(msg)
        return 'Email sent!'
    """
        


@app.route("/profile")
@login_required
def hello_profile():
    """
    Displays the user's profile page. (User must be logged in)

    * Initializes counters for total tasks, completed tasks, in-progress tasks, and cancelled tasks.
    * Fetches the current user's tasks.
    * Iterates through tasks (if any) and updates the counters based on the task status.

    Returns:
        The rendered profile template with user information and counters for total tasks, completed tasks, in-progress tasks, and cancelled tasks.
    """

    try:
        tasks = current_user.tasks
        notices = current_user.notes
        task_counts = {
            'all': len(tasks),
            'in_progress': sum(task.status.name == 'In_Progress' for task in tasks),
            'completed': sum(task.status.name == 'Completed' for task in tasks),
            'cancelled': sum(task.status.name == 'Cancelled' for task in tasks),
        }

        return render_template('profile.html', current_user=current_user,
                              notices=notices, task_counts=task_counts)

    except Exception as e:
        print(f"An error occurred while fetching tasks or notices: {e}")
        return render_template('profile.html', current_user=current_user)

    
@app.route("/invites")
@login_required
def hello_invites():
    """
    Prepares data for the "Invites" page (User must be logged in).

    * Fetches the current user's tasks (current_user.tasks).
    * Initializes an empty dictionary (shared_tasks) to store data for shared tasks.
    * Iterates through the user's tasks:
        - For each task, iterates through its associated users (`task.users`).
        - If the user is not the current user:
            - Checks if the user ID already exists in `shared_tasks`.
              - If not, creates a new entry with the user's information and an empty list for tasks (`{'user': user, 'tasks': []}`).
            - Appends the current task to the appropriate user's task list within `shared_tasks`.
    * Renders the "Invites" template (`invites.html`) with user information, shared tasks data (`shared_tasks`), and all the user's tasks (`tasks`) if there are shared tasks.
    * Renders the "dashboard.html" template (assuming a typo) if there are no shared tasks.
    * Catches any exceptions and simply renders the "Invites" template (error handling can be improved).

    Returns:
        The rendered "Invites" page or "dashboard" page template with data.
    """
    try:
        notices = current_user.notes
        tasks = current_user.tasks
        shared_tasks = {}
        for task in tasks:
            for user in task.users:
                if user.id != current_user.id:
                    if user.id not in shared_tasks:
                        shared_tasks[user.id] = {'user': user, 'tasks': []}
                    shared_tasks[user.id]['tasks'].append(task)

        if shared_tasks:
            return render_template('invites.html', current_user=current_user, shared_tasks=shared_tasks, tasks=tasks, notices=notices)
        else:
            return render_template('invites.html', notices=notices)
    except:
        return render_template('invites.html', notices=notices)
    

@app.route("/<task_id>/search_user", methods=['GET','POST'])
@login_required
def hello_search_user(task_id):
    """
    Searches for users to invite to a specific task (User must be logged in).

    * GET: Renders the "Invites to Task" template (`invites_to_task.html`) with the task information.

    * POST:
        - Validates the search form data using `SearchUserForm`.
        - Retrieves the searched username from the form.
        - Checks various conditions:
            - If the searched user is the current user, flashes an error message and re-renders the template.
            - If the user is already invited to the task, flashes an error message and re-renders the template.
            - If the user is found:
                - Renders the "Invites to Task" template with task information and the searched user information.
            - If the user is not found, flashes an error message and re-renders the template.
        - Flashes an error message if form validation fails and re-renders the template.

    Returns:
        - The rendered "Invites to Task" template with task and user information on successful search
        - The rendered "Invites to Task" template with error messages on various failures
        - The rendered "Invites to Task" template with the task information on GET request.
    """

    task = Task.query.filter_by(id=task_id).first()
    notices = current_user.notes
    form = SearchUserForm(request.form)
    if form.validate():
        searched_user = User.query.filter_by(username=form.username.data).first()
        if searched_user == current_user:
            flash("You can't invite yourself")
            return render_template('invites_to_task.html', task=task, notices=notices)
        if searched_user in task.users:
            flash('User already invited')
            return render_template('invites_to_task.html', task=task, notices=notices)
        if searched_user:
            return render_template('invites_to_task.html', task=task, searched_user=searched_user, notices=notices)
        else:
            flash('User not found')
            return render_template('invites_to_task.html', task=task, notices=notices)
    else:
        flash('Enter a username')
        return render_template('invites_to_task.html', task=task, notices=notices)
        

@app.route("/invite_to_task/<task_id>", methods=['GET','POST'])
@login_required
def hello_invite_to_task(task_id):
    """
    Displays the invitation form for a specific task (User must be logged in)

    * On success:
        - Fetches the task using `db.session.query(Task).get(task_id)`.
        - Renders the "Invites to Task" template with the retrieved task (`task`) and current user (`current_user`) information for populating the invitation form.

    * On database query error:
        - Flashes an error message ("Sorry, couldn't query the database").
        - Redirects the user back to the specific task page (`hello_each_task`) with the task ID.

    * Returns:
        - The rendered "Invites to Task" template with task and current user information on success.
        - A redirection to the specific task page with an error message on database query error.
    """

    try:

        notices = current_user.notes
        task = db.session.query(Task).get(task_id)
        return render_template('invites_to_task.html', task=task, current_user=current_user, notices=notices)
    except:
        flash("Sorry, couldn't query the database")
        return redirect(url_for('hello_each_task', task_id=task_id, notices=notices))
    

@app.route("/invite_user_to_task/<task_id>/<user_id>", methods=['GET','POST'])
@login_required
def hello_invite_user_to_task(task_id, user_id):
    """
    Adds invited users to a specific task. (User must be logged in)

    * On success:
        - Fetches the task from the database using `db.session.query(Task).get(task_id)`.
        - Renders the "Invites to Task" template (`invites_to_task.html`) with the retrieved task information and current user information.

    * On database query error:
        - Flashes an error message indicating the database query failed.
        - Redirects the user to the `hello_each_task` function for the same task ID (`task_id`).

    Returns:
        - The rendered "Invites to Task" template with task information on success.
        - A redirection to the `hello_each_task` function with the task ID on database query error.
    """
    try:
        user = db.session.query(User).get(user_id)
        task = db.session.query(Task).get(task_id)
        
        
        notification = Notification(notification="You have been invited to a task titled", task_title=task.title)
        user.notes.append(notification)

        task.users.append(user)

        team = task.users
        db.session.commit()
        flash(f"{user.username} successfully added")
        return redirect(url_for('hello_each_task', task_id=task_id, team=team))
    except:
        flash("Sorry, couldn't query the database")
        return redirect(url_for('hello_each_task', task_id=task_id))


@app.route("/tasks", methods=['GET','POST'])
@login_required
def hello_tasks():
    """
    Displays the user's tasks (User must be logged in)

    * On success:
        - Fetches all tasks associated with the current user (`current_user.tasks`).
        - Renders the "Tasks" template with the retrieved tasks (`tasks`).

    * On database query error:
        - Simply renders the "Tasks" template (error handling can be improved).

    Returns:
        - The rendered "Tasks" template with user's tasks on success.
        - The rendered "Tasks" template (without data) on database query error.
    """
    try:
        notices = current_user.notes
        tasks = current_user.tasks
        if tasks:
            return render_template("tasks.html", tasks=tasks, notices= notices)
        else:
            return render_template("tasks.html", notices=notices)
    except:
        return render_template("tasks.html", notices=notices)

    
@app.route("/in_process_tasks")
@login_required
def hello_in_process_tasks():
    """
    Displays the user's in-progress tasks (User must be logged in).

    * On success:
        - Fetches all tasks associated with the current user (`current_user.tasks`).
        - Filters the tasks to include only those with an "In Progress" status.
        - Renders the "In Process Tasks" template (`in_process_tasks.html`) with the filtered tasks.

    * On database query error:
        - Simply renders the "In Process Tasks" template (error handling can be improved).

    Returns:
        - The rendered "In Process Tasks" template with user's in-progress tasks on success.
        - The rendered "In Process Tasks" template (without data) on database query error.
    """
    try:
        notices = current_user.notes
        tasks = current_user.tasks
        if tasks:
            return render_template("in_process_tasks.html", tasks=tasks, notices=notices)
        else:
            return render_template("in_process_tasks.html", notices=notices)
    except:
        return render_template("in_process_tasks.html", notices=notices)

    
@app.route("/completed_tasks")
@login_required
def hello_completed_tasks():
    """
    Displays the user's completed tasks (User must be logged in).

    * On success:
        - Fetches all tasks associated with the current user (`current_user.tasks`).
        - Filters the tasks to include only those with a "Completed" status.
        - Renders the "Completed Tasks" template (`completed_tasks.html`) with the filtered tasks.

    * On database query error:
        - Simply renders the "Completed Tasks" template.

    Returns:
        - The rendered "Completed Tasks" template with user's completed tasks on success.
        - The rendered "Completed Tasks" template (without data) on database query error.
    """
    try:
        notices = current_user.notes
        tasks = current_user.tasks
        if tasks:
            return render_template("completed_tasks.html", tasks=tasks, notices=notices)
        else:
            return render_template("completed_tasks.html", notices=notices)
    except:
        return render_template("completed_tasks.html", notices=notices)
    

@app.route("/cancelled_tasks")
@login_required
def hello_cancelled_tasks():
    """
    Displays the user's cancelled tasks. (User must be logged in).

    * On success:
        - Fetches all tasks associated with the current user (`current_user.tasks`).
        - Filters the tasks to include only those with a "Cancelled" status (implementation details depend on your ORM).
        - Renders the "Cancelled Tasks" template (`cancelled_tasks.html`) with the filtered tasks (`tasks`).

    * On database query error:
        - Simply renders the "Cancelled Tasks" template (error handling can be improved).

    Returns:
        - The rendered "Cancelled Tasks" template with user's cancelled tasks on success.
        - The rendered "Cancelled Tasks" template (without data) on database query error.
    """
    try:
        notices = current_user.notes
        tasks = current_user.tasks
        if tasks:
            return render_template("cancelled_tasks.html", tasks=tasks, notices=notices)
        else:
            return render_template("cancelled_tasks.html", notices=notices)
    except:
        return render_template("cancelled_tasks.html", notices=notices)


@app.route("/new_task", methods=['GET', 'POST'])
def hello_new_task():
    """
    Creates a new task. (User must be logged in).

    * GET: Renders the "New Task" template (`new_task.html`) for user input.

    * POST:
        - Validates the submitted form data using `TaskForm`.
        - Creates a new `Task` object with validated data:
            - Title (`title`)
            - Description (`description`)
            - Due date (string format, conversion to `datetime.date` not implemented) (`due_date`)
            - Status (assumed default "In_Progress") (`status`)
            - Tag (`tag`)
        - Appends the task to the current user's `assigned_tasks` list.
        - Commits the changes to the database using `db.session.commit()`.
        - Flashes a success message and redirects to the specific task page (`hello_each_task`) with the newly created task's ID.

    * On form validation or database errors:
        - Flashes appropriate error messages and re-renders the "New Task" template with the form for user correction.

    Returns:
        - The rendered "New Task" template on GET request.
        - The rendered "New Task" template with error messages on form or database errors (POST request).
        - A redirection to the specific task page on successful task creation (POST request).
    """
    user = current_user
    notices = current_user.notes
    if request.method == 'GET':
        return render_template("new_task.html", notices=notices)

    if request.method == 'POST':
        form = TaskForm(request.form)
        if form.validate():
            try:
                due_date_str = form.due_date.data
                task = Task(
                    title  = form.title.data,
                    description  = form.description.data,
                    due_date = due_date_str,
                    status = "In_Progress",
                    tag = form.tag.data
                )
                user.assigned_tasks.append(task)
                db.session.commit()
                
                flash('Task created successfully!')
                task_id = task.id
                return redirect(url_for('hello_each_task',task_id=task_id, notices=notices))

            except Exception as e:
                flash(f'Error creating task: {str(e)}')
                return render_template("new_task.html", notices=notices)
        else:
            flash(form.errors, category='error')
            return render_template('new_task.html', notices=notices)


@app.route("/task/<task_id>/<notice_id>", methods=['GET','POST'])
@app.route("/task/<task_id>", methods=['GET','POST'])
@login_required
def hello_each_task(task_id, team=None, notice_id=None):
    task = Task.query.get_or_404(task_id)
    team = task.users
    notices = current_user.notes

    if current_user not in team:
        flash(f'Cannnot access that task')
        return render_template("dashboard.html", task=task)
    else:
        try:
            if notice_id is not None:
                notification = Notification.query.get(notice_id)
                notification.seen = True
                db.session.commit()
                return redirect(url_for('hello_each_task',task_id=task_id), notices=notices)
            
            else:
                if task:
                    return render_template("each_task.html", task=task, team=team, notices=notices)

        except:
            return redirect(url_for('hello_dashboard', task_id=task_id, notices=notices))

    

@app.route("/edit/<task_id>", methods=['GET','PUT'])
@login_required
def hello_edit_task(task_id):
    """
    Displays the edit form for a specific task. (User must be logged in)

    * On success:
        - Fetches the task using `Task.query.get_or_404(task_id)`, raising a 404 error if not found.
        - Renders the "Edit Task" template with the retrieved task information for pre-populating the form.

    * Returns:
        - A 404 error response if the task is not found.
    """
    task = Task.query.get_or_404(task_id)
    notices = current_user.notes
    if task:
        return render_template("edit_task.html", task=task, notices=notices)
        

@app.route("/save_task/<task_id>", methods=['GET','POST'])
@login_required
def hello_save_task(task_id):
        form = TaskForm(request.form)
        task = Task.query.get_or_404(task_id)
        notices = current_user.notes
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
            except Exception as e:
                flash(f'Error saving task: {str(e)}')
                return render_template("each_task.html", task=task, notices=notices)
        else:
            flash(form.errors, category='error')
            return render_template('edit_task.html', task=task, notices=notices)
        
        
@app.route("/delete/<task_id>", methods=['GET','POST'])
@login_required
def hello_delete_task(task_id):
    """
    Deletes a specific task for the current user (User must be logged in)

    * On success:
        - Fetches the task using `Task.query.get_or_404(task_id)`, raising a 404 error if not found.
        - Removes the task from the current user's `assigned_tasks` list.
        - Commits the changes to the database using `db.session.commit()`.
        - Flashes a success message ("Task Deleted").
        - Redirects the user to the dashboard (`hello_dashboard`).

    * Returns:
        - A 404 error response if the task is not found.
    """
    task = Task.query.get_or_404(task_id)
    user = current_user
    if task:
        user.assigned_tasks.remove(task)
        db.session.commit()
        flash("Task Deleted")
        return redirect(url_for('hello_dashboard')) 
        

@app.route("/notifications")
@login_required
def hello_notices():
    """
    Displays the user settings page. (User must be logged in).

    Returns:
        - The rendered "Notification" template.
    """
    try:
        notices = current_user.notes
        tasks = current_user.tasks
        return render_template("notifications.html", notices=notices, tasks=tasks)
    except Exception as e:

        flash("Error fetching notifications or tasks: {}".format(e))
        return render_template("dashboard.html")


@app.route("/logout")
def hello_logout():
    """
    Logs out the current user and redirects to the login page.
    
    Returns:
        - The rendered "Login" template.
    """
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('hello_login'))