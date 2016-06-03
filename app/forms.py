from flask.ext.wtf import Form
from app.models import Role, User
from wtforms import StringField, BooleanField, PasswordField, HiddenField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email
from app.widgets import ChekBoxTextWidget, SubmitButtonWidget
from flask.ext.babel import Babel, lazy_gettext

def exist(table, column, data):
        test = table.query.filter(column == data).first()
        if test is not None:
            raise ValidationError( lazy_gettext('This %(colname)s is already in use. Please choose another one.', colname=column.name))


def user_exist(form, field):
    return exist(User, User.nickname, field.data)


def email_exist(form, field):
    return exist(User, User.email, field.data)

class DataRequired_lang(DataRequired):
    message=lazy_gettext('This field is required')


class SearchForm(Form):
    text = StringField('search', validators=[DataRequired_lang()])
    find = SubmitField('Find', widget=SubmitButtonWidget(text=lazy_gettext('Find'), glyph='glyphicon-search'))


class PostDeleteForm(Form):
    post_id = HiddenField('post_id', [DataRequired_lang()])
    delete = SubmitField('delete')


class UserDeleteForm(Form):
    user_id = HiddenField('user_id', [DataRequired_lang()])
    delete = SubmitField('delete')


class PostForm(Form):
    post = TextAreaField('post', [DataRequired_lang()])
    send = SubmitField('Send', widget=SubmitButtonWidget(text=lazy_gettext('Send'), glyph=''))


class LoginForm(Form):
    login = StringField('login', [DataRequired_lang()])
    password = PasswordField('password', [DataRequired_lang()])
    remember_me = BooleanField('remember_me', default=False, widget=ChekBoxTextWidget())
    sign_in = SubmitField('Sign In', widget=SubmitButtonWidget(text=lazy_gettext('Sign In'), glyph='glyphicon-log-in'))


class RegisterForm(Form):
    login = StringField('login', [DataRequired_lang(), user_exist])
    email = StringField('email', [DataRequired_lang(), email_exist, Email()])
    password = PasswordField('password',
                             [DataRequired_lang(),
                              EqualTo('password_confirm',message=lazy_gettext('Passwords must match'))])
    password_confirm = PasswordField('password_confirm', [DataRequired_lang()])
    #try:
    #   roles = [(str(role.id), role.role_name) for role in Role.query.all()]
    #except:
    #    roles = [('1', 'empty')]
    #role = SelectField('role', choices=roles)
    about_me = TextAreaField('about me')
    register = SubmitField('Register', widget=SubmitButtonWidget(text=lazy_gettext('Register'), glyph='glyphicon-save'))
