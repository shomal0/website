from flask import Blueprint, render_template
from flask_login import login_required

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    return render_template('home.html')


@views.route('/about')
def about():
    return render_template('about.html')


@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@views.route('/profile_action')
@login_required
def profile_action():
    return render_template('profile_action.html')


@views.route('/change_password')
@login_required
def change_profile():
    return render_template('change_password.html')
