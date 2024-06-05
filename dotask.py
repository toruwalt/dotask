#!/usr/bin/python3
"""My Taskkeeper"""

from flask import Flask, render_template, redirect, url_for
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "1234567890"


@app.route("/")
def hello_world():
    """The homepage"""
    return "<p>Hello, World!</p>"

@app.route("/about")
def hello_about():
    """The about page"""
    return "<p>Hello, World!</p>"

@app.route("/register", methods=['GET', 'POST'])
def hello_register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def hello_login():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
