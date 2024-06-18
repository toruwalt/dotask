from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegisterForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)], )
    password = PasswordField('Password', [
        validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=2, max=35)])
    first_name = StringField('First name', [validators.Length(min=2, max=35)])
    last_name = StringField('Last name', [validators.Length(min=2, max=35)])
    password = PasswordField('New Password', [validators.DataRequired(),
    validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired()])