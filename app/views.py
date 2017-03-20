from flask import render_template
from app import app

@app.route('/')
@app.route('/index')

def index():
   # return "hello, dsli!"
   user = {'nickname': 'dsli'}
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
   return render_template('index.html', title='home', user=user, posts=posts)
