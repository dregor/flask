import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SESSION_TYPE = 'sqlalchemy'

WHOOSH_BASE = os.path.join(basedir, 'search.db')

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

POSTS_PER_PAGE = 10
MAX_SEARCH_RESULTS = 50

# email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'flask.site@gmail.com'
MAIL_PASSWORD = 'xaloo7Do'

# administrator list
INFO_EMAIL = 'flask.site@gmail.com'
ADMINS = ['flask.site@gmail.com']
