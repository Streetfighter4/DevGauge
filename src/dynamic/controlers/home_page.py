from flask import Blueprint
from flask import render_template


home_page_blue_print = Blueprint('home_page', __name__)

@home_page_blue_print.route('/')
def home_page():
    return render_template('home_page.html')
