#-*- coding: utf-8 -*- 
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_restful import Resource, Api
from app import app, db, lm
from forms import LoginForm, RegisterForm
from models import User, Role, Post

@app.before_request
def before():
    g.access_list = [ role.role_name for role in Role.query.all() ]
    g.roles = [ role.role_name for role in current_user.roles ]

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.filter_by(wall_id = current_user.id)
    return render_template('index.html', title = 'Index', posts = posts)

@app.route('/users')
@login_required
def users():
    users = User.query.order_by(User.id)
    return render_template('users.html', title = 'Rsers', users = users)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return standart_login(form)

    return render_template('login.html', title = 'Sign In', form = form)

def standart_login(form):
    user = User.query.filter_by(nickname = form.login.data).first() 
    if user and user.check_password(form.password.data):
        flash( 'Successfull' )
        login_user(user,remember = form.remember_me.data)
        return redirect(request.args.get('next') or url_for('index')) 
    flash(' Bad user! ')
    return redirect( url_for('login') ) 

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegisterForm() 
    if request.method == 'GET':
        return render_template('register.html', title = 'Register', form = form)
    user = User(nickname = form['login'].data, 
                password = form['password'].data,
                email = form['email'].data,
                role = access_list['user']
                )
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first() 
    if user is None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    return render_template('user.html', title='User :' + nickname, user = user)
