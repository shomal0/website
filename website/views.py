from flask import Blueprint, render_template, flash, request, redirect, url_for
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


@views.route('/new_group', methods=['POST', 'GET'])
@login_required
def new_group():
    if request.method == 'POST':
        flash('Group created!', category='success')
        # add group to database
        return redirect(url_for('views.home'))
    return render_template('new_group.html')
