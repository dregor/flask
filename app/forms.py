from flask.ext.wtf import Form
from models import Role
from wtforms import StringField, BooleanField, PasswordField, HiddenField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo


class PostForm(Form):
    post = TextAreaField('post', [DataRequired()])


class LoginForm(Form):
    login = StringField('login', [DataRequired()])
    password = PasswordField('password', [DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(Form):
    login = StringField('login', [DataRequired()])
    email = StringField('email', [DataRequired()])
    password = PasswordField('password', [DataRequired(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('password_confirm', [DataRequired()])
    role = SelectField('role', choices=[(role.id, role.role_name) for role in Role.query.all()])
