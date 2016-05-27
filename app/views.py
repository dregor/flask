from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import LoginForm, RegisterForm, PostForm, PostDeleteForm, UserDeleteForm, SearchForm
from app.models import User, Role, Post
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS
from site_email import send_mail_register


@app.before_request
def before():
    g.search_form = SearchForm()
    if current_user and current_user.is_authenticated:
        current_user.see_you()
        g.roles = [role.role_name for role in current_user.roles]


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html',
                           title='Index')


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    user_delete_form = UserDeleteForm()

    if request.method == 'POST':
        if user_delete_form.validate_on_submit():
            if current_user.have_role('admin'):
                user_tmp = User.query.get(user_delete_form.user_id.data)
                try:
                    user_tmp.delete()
                except Exeption as e:
                    flush('Can\'t delete user error - ' + e, 'danger')
                else:
                    flash('User has been deleted ' + user_tmp.nickname, 'info')
            else:
                flash('You don\'t have an access to do this', 'danger')

        return redirect(request.path)
    user_list = User.query.order_by(User.id)
    return render_template('users.html',
                           title='Users',
                           users=user_list,
                           user_delete_form=user_delete_form)


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
        flash('Successful login.', 'success')
        login_user(user_tmp, remember=form.remember_me.data)
        user_tmp.is_autenticated = True
        db.session.commit()
        return redirect(request.args.get('next') or url_for('index'))
    flash('Login failed!', 'danger')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(nickname=form['login'].data).first() is None:
            user_tmp = User(nickname=form['login'].data,
                            password=form['password'].data,
                            email=form['email'].data,
                            about_me=form['about_me'].data)
            user_tmp.roles.append(Role.query.filter_by(role_name='user').first())
            db.session.add(user_tmp)
            db.session.commit()
            flash('User successfully registered.', 'success')
            # User.query.filter_by(nickname=user_tmp.nickname).first().delete()
            return redirect(url_for('index'))
        else:
            flash('User already exist.', 'danger')
            return redirect(request.path)

    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route('/user/<nickname>', methods=['GET', 'POST'])
@app.route('/user/<nickname>/wall/<int:page>', methods=['GET', 'POST'])
@login_required
def user(nickname, page=1):

    user_tmp = User.query.filter_by(nickname=nickname).first()

    if user_tmp is None:
        flash('User ' + nickname + ' don\'t found.', 'warning')
        return redirect(url_for('index'))

    posts = Post.query.filter_by(wall_id=user_tmp.id).paginate(page, POSTS_PER_PAGE, False)
    post_delete_form = PostDeleteForm()
    post_form = PostForm()

    if post_delete_form.validate_on_submit():
        post_tmp = Post.query.get(post_delete_form.post_id.data)
        if post_tmp.author == current_user or current_user.have_role('admin'):
            try:
                post_tmp.delete()
            except Exception as e:
                flash('Can\'t delete post, error - ' + e, 'danger')
            else:
                flash('Post has been deleted ' + str(post_tmp), 'info')
        else:
            flash('You don\'t have an access to do this', 'danger')
        return redirect(request.path)

    if post_form.validate_on_submit():
        user_tmp.post_on_the_wall(user=current_user,
                                  body=post_form.post.data)
        return redirect(request.path)

    return render_template('user.html',
                           title='User :' + nickname,
                           user=user_tmp,
                           post_form=post_form,
                           post_delete_form=post_delete_form,
                           posts=posts,
                           current_page=page
                           )


@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(request.path)
    return redirect(url_for('search_results', query=g.search_form.text.data))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    posts = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html', query=query, posts=posts)
