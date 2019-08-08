from flask import render_template, request, Blueprint
from reviewit.models import Post
from flask_login import login_required


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	# page = request.args.get('page', 1, type=int)
	# posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
	posts = []
	return render_template('home.html', posts=posts, sidebar=True)

@main.route("/about")
def about():
	return render_template('about.html', title="About")

@main.route("/dashboard")
@login_required
def dashboard():
	return render_template('dashboard.html', title="Dashboard")
