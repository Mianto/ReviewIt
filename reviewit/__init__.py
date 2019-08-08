import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from reviewit.config import Config

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)
	
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	migrate.init_app(app, db)
	

	from reviewit.users.routes import users
	# from reviewit.posts.routes import posts
	from reviewit.main.routes import main
	from reviewit.errors.handlers import errors

	app.register_blueprint(users)
	# app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)
	return app

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host='127.0.0.1', port=5000, use_debugger=True))
