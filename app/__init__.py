from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.restless import APIManager

app = Flask(__name__.split('.')[0])
app.config.from_object('config')

db = SQLAlchemy(app)

rest = APIManager(app, session=db.session)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


