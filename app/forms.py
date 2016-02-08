from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, HiddenField
from wtforms.validators import Required

class LoginForm(Form):
    openid = HiddenField('openid')
    login = TextField('login')
    password = PasswordField('password')
    remember_me = BooleanField('remember_me', default = False)

class RegisterForm(Form):
    login = TextField('login')
    email = TextField('email')
    password = PasswordField('password')
    password_confirm = PasswordField('password_confirm')


