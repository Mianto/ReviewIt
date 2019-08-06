from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from reviewit import current_app, db, bcrypt
from reviewit.models import User, Post
from reviewit.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   ResetRequestForm, ResetPasswordForm, VerifyPasswordForm)
from reviewit.users.utils import save_picture, send_reset_email, send_conf_email

users = Blueprint('users', __name__)


@users.route("/")
def hello():
	return render_template('base.html', sidebar=True)



@users.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if request.method=='POST':	
		if form.validate_on_submit():
			print(123)
			hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = User(email = form.email.data, username = form.username.data, password = hash_pwd)
			db.session.add(user)
			db.session.commit()
			try:
				send_conf_email(user)
				flash(f'An confirmation link has been sent to {user.email}', 'info')
			except:
				flash(f'Something went wrong', 'danger')
			return redirect(url_for('users.login'))

	return render_template('register.html', title="Register", form = form)


@users.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if request.method=='POST':	
		if form.validate_on_submit():
			user = User.query.filter_by(email = form.email.data).first()
			if user and bcrypt.check_password_hash(user.password, form.password.data) and user.confirmed:
				login_user(user, remember=form.remember.data)
				flash(f'You have logged in !!', 'success')
				next_page = request.args.get('next')
				if next_page:
					return redirect(next_page)
				else:
					return redirect(url_for('main.home'))
			else:
				if user and not user.confirmed:
					flash(f'Email confirmation is not done yet', 'danger')
				else:
					flash(f'Login Unsuccessful. Please check username and password !!', 'danger')


	return render_template('login.html', title="Login", form = form)

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route("/conf_email/<token>", methods=['GET', 'POST'])
def conf_email(token):
	if current_user.is_authenticated:
		flash(f'Logout before using Email Confirmation Link')
		return redirect(url_for('main.home'))

	user = User.verify_conf_token(token)

	if not user:
		flash(f'This URL is either invalid or expired.', 'warning')
	else:
		flash(f'Email Confirmation is successfully done. Now try logging in', 'success')
		user.confirmed = True
		db.session.commit()

	return redirect(url_for('users.login'))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		form = VerifyPasswordForm()
		if form.validate_on_submit():
			return redirect(url_for('users.reset_token', token=-1))
		else:
			flash(f'The password you typed doesn\'t match with your existing password', 'warning')
			return redirect(url_for('users.account', uname=current_user.username))
	else:
		form = ResetRequestForm()
		if form.validate_on_submit():
			user = User.query.filter_by(email=form.email.data).first()
			send_reset_email(user)
			flash(f'An email has been sent with instructions to reset your password', 'info')
			return redirect(url_for('users.login'))

	return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	form = ResetPasswordForm()
	if current_user.is_authenticated:
		if form.validate_on_submit():
			current_user.password = form.password.data
			db.session.commit()
			return redirect(url_for('users.account', uname=current_user.username))
	else:
		user = User.verify_reset_token(token)
		if not user:
			flash(f'This URL is either invalid or expired.', 'warning')
			return redirect(url_for('users.login'))
		
		if form.validate_on_submit():
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user.password = hashed_password
			db.session.commit()
			flash('Your password has been updated! You are now able to log in', 'success')
			return redirect(url_for('users.login'))

	return render_template('reset_token.html', title='Reset Password', form=form)



@users.route("/account/<string:uname>", methods=['GET', 'POST'])
def account(uname):
	
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=uname).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)

	if current_user.is_authenticated and current_user.username == uname:
		form = UpdateAccountForm()
		pForm = VerifyPasswordForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				if form.picture.data:
					picture_file = save_picture(form.picture.data)
					old_picture = current_user.image_file
					current_user.image_file = picture_file
					if old_picture != "default.jpg":
						file_path = os.path.join(current_app.root_path, 'static', 'profile_pics', old_picture)
						os.remove(file_path)
						print("Old Picture Removed")
				current_user.username = form.username.data
				current_user.email = form.email.data
				db.session.commit()
				flash('Your account has been updated!', 'success')
				return redirect(url_for('users.account', uname=current_user.username))
		elif request.method == 'GET':
			form.username.data = current_user.username
			form.email.data = current_user.email

		return render_template('account.html', title='Account', form=form, pForm=pForm, account=current_user, posts=posts, sidebar=True)
	else:
		form = None
		return render_template('account.html', title='Account', account=user, posts=posts, sidebar=True)

