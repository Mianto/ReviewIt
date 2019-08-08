from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from reviewit import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(60), nullable=False)
	lname = db.Column(db.String(60), nullable=False)
	username = db.Column(db.String(60), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	designation = db.Column(db.String(60), nullable=True)
	company = db.Column(db.String(60), nullable=True)
	website = db.Column(db.String(60), nullable=True)
	description = db.Column(db.String(400), nullable=True)
	confirmed = db.Column(db.Boolean(), nullable=False, default=False, server_default="false")
	is_admin = db.Column(db.Boolean(), nullable=False, default=False, server_default="false")

	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f'User ({self.id}, {self.username}, {self.email})'

	def get_reset_token(self, expires_sec=7200):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def get_conf_token(self, expires_sec=7200):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'email': self.email}).decode('utf-8')

	@staticmethod
	def verify_conf_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		# try:
		email = s.loads(token)['email']
		# except:
		# 	return None
		print(email)
		return User.query.filter_by(email=email).first()





class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	def __repr__(self):
		return f"Post ({self.id}, {self.title}, {self.date_posted})"