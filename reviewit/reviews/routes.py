from flask import current_app, render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from reviewit import db, bcrypt
from reviewit.models import User, ReviewSection, Review
from reviewit.reviews.forms import ReviewForm, MakeSection
from reviewit.reviews.utils import verify_section
from functools import wraps
from datetime import datetime
from urllib.parse import unquote
from flask import jsonify


reviews = Blueprint('reviews', __name__)




@reviews.route('/section/add', methods=['GET', 'POST'])
@login_required
def make_section():
	form = MakeSection()

	if form.validate_on_submit():
		title = form.title.data
		placeholder = form.placeholder.data
		heading = form.heading.data
		section_id = bcrypt.generate_password_hash((current_user.username+str(datetime.utcnow)).encode('utf-8')).decode('utf-8')
		new_section = ReviewSection(section_id = section_id, campaign_title = title, heading=heading, placeholder = placeholder, owner=current_user)
		print(new_section)
		db.session.add(new_section)
		db.session.commit()
		flash('Your review section has been successfully posted', 'success')
		return redirect(url_for('reviews.review_sections'))
	else:

		form.heading.render_kw['placeholder'] = 'Comments'
		form.placeholder.render_kw['placeholder'] ='ReviewIt here ....'

	return render_template('make_section.html', form=form, title='Make Review Section')

@reviews.route('/section/', methods=['GET'])
@login_required
def review_sections():

	sections = ReviewSection.query.all()
	print(sections)
	return render_template('review_sections.html', sections=sections, title='Review Sections')


@reviews.route('/section/<string:section_id>/view_reviews', methods=['GET', 'POST'])
@login_required
def see_reviews(section_id):
	section_id = unquote(section_id)
	if(verify_section(section_id)):
		review_section_id = ReviewSection.query.filter_by(section_id=section_id).first()
		reviews = Review.query.filter_by(section_id=review_section_id.id).all()
		print(reviews)
		campaign = ReviewSection.query.filter_by(section_id=section_id).first().campaign_title
		return render_template('see_reviews.html', reviews=reviews, campaign=campaign)
	else:
		return "You came to the wrong page. Please inform <strong>Team ReviewIt<strong> about it"


@reviews.route("/section/<string:section_id>", methods=['GET'])
def show_section(section_id):
	section_id = unquote(section_id)
	if verify_section(section_id):
		form = ReviewForm()
		section = ReviewSection.query.filter_by(section_id=section_id).first()

		form.review_text.render_kw['placeholder'] = section.placeholder

		reviews = Review.query.filter_by(section_id=section_id)
		print(reviews)
		heading = section.heading

		return render_template('comment_section.html', form=form, id=section_id, reviews=reviews, heading=heading)
	else:
		return 'Contact Us @ Team ReviewIt'

@reviews.route("/section/<string:section_id>/add", methods=['POST'])
def add_review(section_id):
	section_id = unquote(section_id)
	response = {}
	if verify_section(section_id):
		form = ReviewForm()
		
		if form.validate():
			try:
				section = ReviewSection.query.filter_by(section_id=section_id).first()
				print(section,"skdjfshkfhdkjf")
				new_review = Review(reviewer=form.reviewer.data,
								product_id=form.product_id.data,
								reviewer_email=form.reviewer_email.data,
								review_text=form.review_text.data,
								review_section=section)
				db.session.add(new_review)
				db.session.commit()
				response['msg_type'] = 'success'
				response['msg'] = 'Review added successfully'
			except Exception as e:
				print(e)
				response['msg_type'] = 'danger'
				response['msg'] = 'Something went wrong ...'
		else:
			response['msg_type'] = 'danger'
			response['msg'] = form.errors
	else:
		
		response['msg_type'] = 'danger'
		response['msg'] = 'The review section is not valid'
	return jsonify(response)