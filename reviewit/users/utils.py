
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from reviewit import mail

def save_picture(image_file):

	random_hex = secrets.token_hex(15)

	_, f_ext = os.path.splitext(image_file.filename)

	picture_fname = current_user.username + "-" + random_hex + f_ext

	picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics', picture_fname)

	# Resizing the Image File
	output_size = (125, 125)
	i = Image.open(image_file)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fname

def send_conf_email(user):
    token = user.get_conf_token()
    msg = Message('Email Confirmation Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To confirm your email address, visit the following link:
{url_for('users.conf_email', token=token, _external=True)}

***Please note that the email confirmation link will expire in 2 hours***
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

***Please note that the password reset token will expire in 2 hours***
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)