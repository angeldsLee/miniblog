from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

# @app.route('/')
# @app.route('/index')
@app.route('/login', methods=['get', 'post'])

# def index():
#    # return "hello, dsli!"
#    user = {'nickname': 'dsli'}
#    posts = [  # fake array of posts
#         { 
#             'author': {'nickname': 'John'}, 
#             'body': 'Beautiful day in Portland!' 
#         },
#         { 
#             'author': {'nickname': 'Susan'}, 
#             'body': 'The Avengers movie was so cool!' 
#         }
#     ]
#    return render_template('index.html', title='home', user=user, posts=posts

def login():
  form = LoginForm()
  return render_template('login.html', title="Sing in", form=form)