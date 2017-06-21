from flask import Flask
import logging
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.restless import APIManager
from flask.ext.mail import Mail
from flask.ext.assets import Environment, Bundle
from app.helpers import momentjs, CustomJSONEncoder
from datetime import datetime
from flask.ext.babel import Babel, lazy_gettext
import os, sys
from config import *

sys.path.append(os.path.join(basedir, 'app'))

app = Flask(__name__.split('.')[0])

app.json_encoder = CustomJSONEncoder

app.config.from_object('config')

app.jinja_env.globals['momentjs'] = momentjs
app.jinja_env.globals['date_now'] = datetime.utcnow()

app.logger.setLevel(logging.INFO)

mail = Mail(app)

babel = Babel(app)

db = SQLAlchemy(app)

rest = APIManager(app, session=db.session)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message_category = "info"
lm.login_message = lazy_gettext('Please log in to access this page.')


log_file_name = os.path.join(basedir, 'debug.log')

assets = Environment(app)

js = Bundle('js/moment-with-locales.js',
            'js/jquery.cookie.js',
            'js/bootstrap.js',
            'js/helpers.js',
#            filters='jsmin',
            output='gen/jsall.js')

css = Bundle('css/bootstrap.css',
            filters='cssmin',
            output='gen/cssall.css')

css_profile = Bundle('css/profile.css',
            filters='cssmin',
            output='gen/profile.css')


assets.register('js', js)
assets.register('css', css)
assets.register('cssprofile', css_profile)


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
