from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from reviewit import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, unique=True, primary_key=True)
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

	review_sections = db.relationship('ReviewSection', backref='owner', lazy=True)



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


class ReviewSection(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	section_id = db.Column(db.String(500), unique=True)
	campaign_title = db.Column(db.String(60), default='Campaign', server_default='Campaign')
	heading = db.Column(db.String(60), nullable=False, default='Reviews', server_default='Reviews')
	placeholder = db.Column(db.String(400), nullable=False, default="ReviewIt here ...", server_default="ReviewIt here ....")
	label_1 = db.Column(db.String(60), nullable=True)
	label_2 = db.Column(db.String(60), nullable=True)
	label_3 = db.Column(db.String(60), nullable=True)
	label_4 = db.Column(db.String(60), nullable=True)
	label_5 = db.Column(db.String(60), nullable=True)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	reviews = db.relationship('Review', backref='review_section', lazy=True)



	def __repr__(self):
		return f'Review Section ({self.id}, {self.owner.username}, {self.owner.company})'


class Review(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	reviewer = db.Column(db.String(60), nullable=False)
	reviewer_email = db.Column(db.String(100), nullable=False, default='howdy@xyz.com', server_default='howdy@xyz.com')
	product_id = db.Column(db.String(600), nullable=False, default='Nothing', server_default='Nothing')
	review_text = db.Column(db.String(400), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	upvotes = db.Column(db.Integer, default=0, server_default='0')
	downvotes = db.Column(db.Integer, default=0, server_default='0')
	label_1 = db.Column(db.Integer, default=0, server_default='0')
	label_2 = db.Column(db.Integer, default=0, server_default='0')
	label_3 = db.Column(db.Integer, default=0, server_default='0')
	label_4 = db.Column(db.Integer, default=0, server_default='0')
	label_5 = db.Column(db.Integer, default=0, server_default='0')

	status = db.Column(db.String(60))

	section_id = db.Column(db.Integer, db.ForeignKey('review_section.id'), nullable=False)

	def __repr__(self):
		return f'Review ({self.id}, {self.review_section.owner.username}, {self.review_section.owner.company})'
