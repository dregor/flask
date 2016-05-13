from flask import Flask
import logging
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.restless import APIManager
from flask.ext.mail import Mail
import os, sys
from config import *

sys.path.append(os.path.join(basedir, 'app'))

app = Flask(__name__.split('.')[0])
app.config.from_object('config')

app.logger.setLevel(logging.INFO)

mail = Mail(app)

db = SQLAlchemy(app)

rest = APIManager(app, session=db.session)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

log_file_name = os.path.join(basedir, 'log/debug.log')


def log_to_file():
    file_handler = RotatingFileHandler(log_file_name, 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('site startup')

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    if not os.path.isfile(log_file_name):
        try:
            open(log_file_name, 'w').close()
        except OSError as e:
            print('can\'t create log file')
            print(e)
        else:
            log_to_file()
    else:
        log_to_file()
