from flask import render_template, request, Blueprint
from flask_login import login_required


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	return render_template('home.html', sidebar=True)

@main.route("/about")
def about():
	return render_template('about.html', title="About")

@main.route("/dashboard")
@login_required
def dashboard():
	return render_template('dashboard.html', title="Dashboard")
