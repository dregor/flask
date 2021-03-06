from app import db, rest, app
from datetime import datetime
from hashlib import md5
# from sqlalchemy.exc import NoSuchTableError
import flask.ext.whooshalchemy as whooshalchemy

from werkzeug.security import generate_password_hash, check_password_hash


role_association = db.Table('Role_association',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                            db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy='dynamic', foreign_keys='Post.user_id')
    wall = db.relationship('Post', backref='wall_owner', lazy='dynamic', foreign_keys='Post.wall_id')
    roles = db.relationship('Role', backref='user', secondary=role_association)
    sessions = db.relationship('Session', backref='user')
    last_seen = db.Column(db.DateTime)
    about_me = db.Column(db.String(140))
    # is_active = db.Column(db.Boolean)
    # is_anonymous = db.Column(db.Boolean)
    # is_authenticated = db.Column(db.Boolean)

    def __init__(self, password, **kwargs):
        password_ = generate_password_hash(password)
        super(User, self).__init__(password=password_, **kwargs)

    def post_on_the_wall(self, user, body):
        db.session.add(Post(author=user, wall_owner=self, body=body, timestamp=datetime.utcnow()))
        db.session.commit()

    def all_roles(self):
        return [role.role_name for role in self.roles]

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode('utf-8')).hexdigest() + '?d=mm&s=' + str(size)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id

    def see_you(self):
        self.last_seen = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def have_role(self, role_name):
        return True if Role.query.filter_by(role_name=role_name).first() in self.roles else False

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    wall_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Post %r>' % (self.body)

    def __str__(self):
        return '<Post %r>' % (self.id)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(140), unique=True)

    def __repr__(self):
        return '<Role %r>' % (self.role_name)

    def all_roles(self):
        return self.query.all()


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_hash = db.Column(db.String(120), unique=True)

rest.create_api(User, methods=['GET', 'POST', 'DELETE'])  # , results_per_page=1)
rest.create_api(User, collection_name='user_by_name', primary_key='nickname', methods=['GET', 'POST', 'DELETE'])
rest.create_api(Role, methods=['GET', 'POST', 'DELETE'])

#Default roles :
# if Role.query.first() is None:
#     for item in ['admin', 'user']:
#         db.session.add(Role(role_name=item))
#         db.session.commit()

whooshalchemy.whoosh_index(app, Post)
