import urllib.parse
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', url=urllib.parse.urlparse(request.url))


@auth.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(name) < 2:
            flash('Name must have more than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must have at least 8 characters.', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))
    return render_template('sign_up.html', url=urllib.parse.urlparse(request.url))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out', category='info')
    return redirect(url_for('views.about'))


@auth.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
    if request.method == 'POST':
        email = current_user.email
        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')
        if len(new_password1) < 7:
            flash('Password must have at least 8 characters.', category='error')
        elif new_password1 != new_password2:
            flash('Password don\'t match.', category='error')
        else:
            flash('Password changed!', category='success')
            update_password = User.query.filter_by(email=email).first()
            update_password.password = generate_password_hash(new_password1)
            db.session.commit()

            return redirect(url_for('views.home'))
    return render_template('change_password.html', url=urllib.parse.urlparse(request.url))
