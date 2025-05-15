''' 
Similar to views.py, but for distinction we call it views.py
It has a similar role but it only handles error pages.
Serves the views of the error pages
'''

from flask import Blueprint, render_template
error_pages = Blueprint('error_pages', __name__)

@error_pages.app_errorhandler(404)
def error_404(error):
    # We are not only returning the error page, but a touple that contains the error code as well
    return render_template('error_pages/404.html') , 404

@error_pages.app_errorhandler(403)
def error_403():
    return render_template('error_pages/403.html') , 403