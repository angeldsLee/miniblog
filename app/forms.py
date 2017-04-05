from flask_wtf import Form 
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
	openid = StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class EditForm(object):
	"""docstring for EditForm"""
	def __init__(self, arg):
		nickname = StringField('nickname', validators=[DataRequired()])
		about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
		