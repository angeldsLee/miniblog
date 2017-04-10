from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm, EditForm
from .models import User
from datetime import datetime


@lm.user_loader
def laod_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:  # before_request handler will update the time in the database.
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template('index.html', 
                            title='home', 
                            user=user, 
                            posts=posts)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated: # if a user is already logged in
        return redirect(url_for('index'))
    form = LoginForm()
    # print "form = LoginForm()"
    if form.validate_on_submit():
        # print "validate_on_submit"
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email']) # trigger authentication

    # print "not pass validate_on_submit"
    return render_template('login.html',
                            title='Sign In',
                            form=form,
                            providers=app.config['OPENID_PROVIDERS'])

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('your changes have been saved')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    # print "dsli user" 
    # print user
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author' : user, 'body' : 'test post #1'},
        {'author' : user, 'body' : 'test post #2'}
    ]
    return render_template('user.html',
                            user=user,
                            posts=posts)


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login, please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first() #  search our database for the email provided
    if user is None: # add a new user to our database
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    # return redirect(url_for('index'))
    return redirect(request.args.get('next') or url_for('index'))
    # redirect to the next page, or the index page if a next page was not provided in the request



@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500   












