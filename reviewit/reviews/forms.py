from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL, ValidationError
from flask_login import current_user
from reviewit import bcrypt
from reviewit.models import User


class MakeSection(FlaskForm):
	
	title = StringField('Campaign Name', render_kw={'placeholder':'Campaign Name'},
										validators=[DataRequired()])

	heading = StringField('Heading', render_kw={'placeholder':'Heading'})

	placeholder = StringField('Review Placeholder', render_kw={'placeholder':'Review Placeholder'})

	submit = SubmitField('Post')

class ReviewForm(FlaskForm):
	
	product_id = StringField('Product Id', render_kw={'placeholder': 'Product Id'}, validators=[DataRequired()])


	reviewer = StringField('Name', render_kw={'placeholder':'Name'}, 
										validators = [DataRequired()])

	reviewer_email = StringField('Email', render_kw={'placeholder':'Email Address'}, 
										validators = [DataRequired(), Email()])

	review_text = TextAreaField('Review', render_kw={'placeholder': 'Review goes here'}, 
										validators = [DataRequired(), Length(min=2, max=60)])

	submit = SubmitField('Post')