from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from reviewit import bcrypt
from reviewit.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', render_kw={'placeholder':'Username'}, 
										validators = [DataRequired(),Length(min=2, max=60)])

	email = StringField('Email', render_kw={'placeholder':'Email Address'}, validators = [DataRequired(),Email()])

	password = PasswordField('Password', render_kw={'placeholder':'Password'}, 
										validators = [DataRequired()])

	confirmPassword = PasswordField('Confirm Password', render_kw={'placeholder':'Confirm Password'}, 
										validators = [DataRequired(),EqualTo('password')])

	submit = SubmitField('Sign Up')

	# Check unique user
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError(f'{username.data} is already taken. Retry with a different one')

	# Check unique email
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError(f'{email.data} is already taken. Retry with a different one')


class LoginForm(FlaskForm):
	
	email = StringField('Email', render_kw={'placeholder':'Email'}, 
										validators = [DataRequired(),Email()])

	password = PasswordField('Password', render_kw={'placeholder':'Password'}, 
										validators = [DataRequired()])

	remember = BooleanField('Remember Me')

	submit = SubmitField('Sign Up')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', render_kw={'placeholder':'Username'}, 
										validators = [DataRequired(),Length(min=2, max=60)])

	email = StringField('Email', render_kw={'placeholder':'Email Address'}, 
										validators = [DataRequired(),Email()])
	picture = FileField('Update Profile Picture', render_kw={'placeholder':'.jpg, .png allowed'}, validators=[FileAllowed(['jpg', 'png'])])
    
	submit = SubmitField('Update')

	# Check unique user
	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError(f'{username.data} is already taken. Retry with a different one')

	# Check unique email
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError(f'{email.data} is already taken. Retry with a different one')

class ResetRequestForm(FlaskForm):
	email = StringField('Email', render_kw={'placeholder':'Registered Email'}, 
										validators = [DataRequired(),Email()])

	submit = SubmitField('Request Password Reset')

	# Check registered email
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError(f'No account has been found registered with {email.data}')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', render_kw={'placeholder':'Password'}, 
										validators = [DataRequired()])

	confirmPassword = PasswordField('Confirm Password', render_kw={'placeholder':'Confirm Password'}, 
										validators = [DataRequired(),EqualTo('password')])

	submit = SubmitField('Reset Password')

class VerifyPasswordForm(FlaskForm):
	password = PasswordField('Password', render_kw={'placeholder':'Password'}, 
										validators = [DataRequired()])

	submit = SubmitField('Reset Password')

	# Validate current password
	def validate_password(self, password):
		if not bcrypt.check_password_hash(current_user.password, password.data):
			raise ValidationError(f'The password you typed does not match with your existing password')
