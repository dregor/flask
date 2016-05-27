from flask.ext.wtf import Form
from app.models import Role, User
from wtforms import StringField, BooleanField, PasswordField, HiddenField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from app.widgets import ChekBoxTextWidget


def exist(table, column, data):
        test = table.query.filter(column == data).first()
        if test is not None:
            raise ValidationError('This ' + column.name + ' is already in use. Please choose another one.')


def user_exist(form, field):
    return exist(User, User.nickname, field.data)


def email_exist(form, field):
    return exist(User, User.email, field.data)


class SearchForm(Form):
    text = StringField('search', validators=[DataRequired()])
    find = SubmitField('Find')


class PostDeleteForm(Form):
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
    remember_me = BooleanField('remember_me', default=False, widget=ChekBoxTextWidget())
    sign_in = SubmitField('Sign In')


class RegisterForm(Form):
    login = StringField('login', [DataRequired(), user_exist])
    email = StringField('email', [DataRequired(), email_exist, Email()])
    password = PasswordField('password', [DataRequired(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('password_confirm', [DataRequired()])
    #try:
    #   roles = [(str(role.id), role.role_name) for role in Role.query.all()]
    #except:
    #    roles = [('1', 'empty')]
    #role = SelectField('role', choices=roles)
    about_me = TextAreaField('about me')
    register = SubmitField('Register')
