from app import db
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

role_association = db.Table('Role_association', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(255))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic', foreign_keys='Post.user_id' )
    wall = db.relationship('Post', lazy = 'dynamic', foreign_keys='Post.wall_id' )
    roles = db.relationship('Role', backref='user', secondary=role_association)
    last_seen = db.Column(db.DateTime)
    about_me = db.Column(db.String(140))
    is_active = db.Column(db.Boolean)
    is_anonymous = db.Column(db.Boolean)


    def __init__(self, password, **kwargs):
        password_ = generate_password_hash(password)
        super(User, self).__init__(password = password_, **kwargs)

    def all_roles(self):
        pass

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    wall_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    role_name = db.Column(db.String(140))

    def __repr__(self):
        return '<Role %r>' % (self.role_name)


