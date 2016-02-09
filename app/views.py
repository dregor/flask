#*- coding: utf-8 -*- 
from flask import render_template, flash, redirect,session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, RegisterForm
from models import User, ROLE_USER, ROLE_ADMIN

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': { 'nickname': 'Jhon' },
            'body': 'fuck it'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'bullshit'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        if form.openid.data != '':
            return oid_login(form) 
        else:
            return standart_login(form)

    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

def standart_login(form):
    user = User.query.filter_by(nickname = form.login.data).first()
    if user.check_password(form.password.data):
        flash( 'Successfull' )
        login_user(user,remember = True)
        return redirect(request.args.get('next') or url_for('index')) 
    flash(' Bad user! ')
    return redirect( url_for('login') ) 


def oid_login(form):
    return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])

def standart_after_login():
    pass

def oid_after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, password = 'empty', email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@oid.after_login
def after_login(resp = None):
    if resp is None:
        return standart_after_login()
    else:
        return oid_after_login(resp)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegisterForm() 
    if request.method == 'GET':
        return render_template('register.html', form = form)
    user = User(nickname = form['login'].data, password = form['password'].data, email = form['email'].data, role = ROLE_USER)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('index'))
