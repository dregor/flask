from flask.ext.wtf import Form
from app.models import Role
from wtforms import StringField, BooleanField, PasswordField, HiddenField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class PostViewForm(Form):
    post_id = HiddenField('post_id', [DataRequired()])
    delete = SubmitField('delete')


class UserDeleteForm(Form):
    user_id = HiddenField('user_id', [DataRequired()])
    delete = SubmitField('delete')


class PostForm(Form):
    post = TextAreaField('post', [DataRequired()])
    send = SubmitField('Send')


class LoginForm(Form):
    login = StringField('login', [DataRequired()])
    password = PasswordField('password', [DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    sign_in = SubmitField('Sign In')


class RegisterForm(Form):
    login = StringField('login', [DataRequired()])
    email = StringField('email', [DataRequired()])
    password = PasswordField('password', [DataRequired(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('password_confirm', [DataRequired()])
    role = SelectField('role', choices=[(role.id, role.role_name) for role in Role.query.all()])
    about_me = TextAreaField('about me')
    register = SubmitField('Register')
