#-*- coding: utf-8 -*- 
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_restful import Resource, Api
from app import app, db, lm
from forms import LoginForm, RegisterForm, PostForm
from models import User, Role, Post

@app.before_request
def before():
    if current_user and current_user.is_authenticated:
        current_user.see_you()
        g.roles = [role.role_name for role in current_user.roles]
    #g.access_list = [ role.role_name for role in Role.query.all() ]


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    posts = Post.query.filter_by(wall_id=current_user.id)
    post_form = PostForm()
    #flash(Post(author=current_user, wall_owner=current_user, body=post_form.post.data))

    if post_form.validate_on_submit():
        current_user.post_on_the_wall(user=current_user, body=post_form.post.data)
        return redirect(url_for('index'))

    return render_template('index.html', title='Index', post_form=post_form, posts=posts)


@app.route('/users')
@login_required
def users():
    user_list = User.query.order_by(User.id)
    return render_template('users.html', title='Users', users=user_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return standard_login(form)

    return render_template('login.html', title='Sign In', form=form)


def standard_login(form):
    user_tmp = User.query.filter_by(nickname=form.login.data).first()
    if user_tmp and user_tmp.check_password(form.password.data):
        flash('Successful')
        login_user(user_tmp, remember=form.remember_me.data)
        user_tmp.is_autenticated = True
        db.session.commit()
        return redirect(request.args.get('next') or url_for('index')) 
    flash(' Bad user! ')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm() 
    if request.method == 'GET':
        return render_template('register.html', title = 'Register', form = form)
    user_tmp = User(nickname=form['login'].data,
                    password=form['password'].data,
                    email=form['email'].data,
                    )
    user_tmp.roles.append(Role.query.get(form['role'].data))
    db.session.add(user_tmp)
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
    return render_template('user.html', title='User :' + nickname, user=user)



