from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, HiddenField
from wtforms.validators import Required, EqualTo

class LoginForm(Form):
    login = TextField('login', [Required()])
    password = PasswordField('password', [Required()])
    remember_me = BooleanField('remember_me', default = False)

class RegisterForm(Form):
    login = TextField('login', [Required()])
    email = TextField('email', [Required()])
    password = PasswordField('password', [Required(), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('password_confirm', [Required()])


