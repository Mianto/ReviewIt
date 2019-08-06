from flask import Blueprint, render_template

errors = Blueprint('erros', __name__)

@errors.app_errorhandler(404)
def error_404(error):
	code = 404
	message = 'Oops. Page Not Found'
	return render_template('error_handler.html', message=message, code=code)

@errors.app_errorhandler(403)
def error_403(error):
	code = 403
	message = 'You are forbidden to do that'
	return render_template('error_handler.html', message=message, code=code)


@errors.app_errorhandler(500)
def error_500(error):
	code = 500
	message = 'Something went wrong. Please try after few minutes'
	return render_template('error_handler.html', message=message, code=code)