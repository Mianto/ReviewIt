import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from reviewit.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand



def current_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from reviewit.users.routes import users
	# from reviewit.posts.routes import posts
	# from reviewit.main.routes import main
	from reviewit.errors.handlers import errors

	app.register_blueprint(users)
	# app.register_blueprint(posts)
	# app.register_blueprint(main)
	app.register_blueprint(errors)
	
	return app

migrate = Migrate(current_app, db)
manager = Manager(current_app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host='127.0.0.1', port=5000, use_debugger=True))