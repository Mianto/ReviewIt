from flask import render_template, request, Blueprint
from flask_login import login_required

from .data_processing import sentiment_analyzer

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	return render_template('home.html', sidebar=True)

@main.route("/about")
def about():
	return render_template('about.html', title="About")

@main.route("/dashboard")
def dashboard():
	result = sentiment_analyzer(r'C:\Users\Siddhant\Downloads\data\imdb_master.csv')
	return render_template('dashboard.html', title="Dashboard", result=result)
