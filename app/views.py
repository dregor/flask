#-*- coding: utf-8 -*- 
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import LoginForm, RegisterForm, PostForm, PostViewForm
from app.models import User, Role, Post

@app.before_request
def before():
    if current_user and current_user.is_authenticated:
        current_user.see_you()
        g.roles = [role.role_name for role in current_user.roles]
    #g.access_list = [ role.role_name for role in Role.query.all() ]


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html',
                           title='Index')


@app.route('/users')
@login_required
def users():
    user_list = User.query.order_by(User.id)
    return render_template('users.html',
                           title='Users',
                           users=user_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return standard_login(form)

    return render_template('login.html',
                           title='Sign In',
                           form=form)


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
        return render_template('register.html',
                               title='Register',
                               form=form)

    user_tmp = User(nickname=form['login'].data,
                    password=form['password'].data,
                    email=form['email'].data,
                    )
    user_tmp.roles.append(Role.query.get(form['role'].data))
    db.session.add(user_tmp)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('index'))


@app.route('/user/<nickname>', methods=['GET', 'POST'])
@login_required
def user(nickname):

    user_tmp = User.query.filter_by(nickname=nickname).first()

    if user_tmp is None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))

    posts = Post.query.filter_by(wall_id=user_tmp.id)
    post_view_form = PostViewForm()
    post_form = PostForm()

    if post_view_form.validate_on_submit():
        Post.query.get(post_view_form.post_id.data).delete()
        flash(Post.query.get(post_view_form.post_id.data))
        return redirect(request.path)

    if post_form.validate_on_submit():
        user_tmp.post_on_the_wall(user=current_user,
                                  body=post_form.post.data)
        return redirect(request.path)

    return render_template('user.html',
                           title='User :' + nickname,
                           user=user_tmp,
                           post_form=post_form,
                           post_view_form=post_view_form,
                           posts=posts
                           )



