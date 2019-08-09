from urllib.parse import unquote
from reviewit.models import ReviewSection

def verify_section(section_id):
	section_id = unquote(section_id)
	section = ReviewSection.query.filter_by(section_id=section_id).first()
	# print(section)
	if section:
		return True
	else:
		return False