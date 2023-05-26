import json
import urllib.parse
from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from flask.json import jsonify
from flask_login import login_required, current_user

from . import db
from .models import Group, Note, User

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    username = current_user.name
    user_name = User.query.filter_by(name=username).first()
    return render_template('home.html', url=urllib.parse.urlparse(request.url), groups=user_name.groups)


@views.route('/group', methods=['POST', 'GET'])
@login_required
def group():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) <= 1:
            flash('Note is too short!', category='error')
        elif len(note) >= 100:
            flash('Note is too long!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('text sent!', category='success')
    # group_name =
    username = current_user.name
    user_name = User.query.filter_by(name=username).first()
    return render_template('group.html', user=current_user, url=urllib.parse.urlparse(request.url), groups=user_name.groups)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['note_id']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/about')
def about():
    return render_template('about.html', url=urllib.parse.urlparse(request.url))


@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', url=urllib.parse.urlparse(request.url))


@views.route('/profile_action')
@login_required
def profile_action():
    return render_template('profile_action.html', url=urllib.parse.urlparse(request.url))


@views.route('/new_group', methods=['POST', 'GET'])
@login_required
def new_group():
    if request.method == 'POST':
        group_name = request.form.get('Group_Name')
        create_group = Group(name=group_name)
        db.session.add(create_group)
        db.session.commit()
        session['group_name'] = group_name
        return redirect(url_for('views.add_members'))
    return render_template('new_group.html', url=urllib.parse.urlparse(request.url))


@views.route('/add_members', methods=['POST', 'GET'])
@login_required
def add_members():
    if request.method == 'POST':
        if request.form['submit_button'] == 'add_user':
            name = request.form.get('name')
            name_in_db = User.query.filter_by(name=name).first()
            if name_in_db:
                group_name = session['group_name']
                db_group = Group.query.filter_by(name=group_name).first()
                name_in_db.groups.append(db_group)
                db.session.add(name_in_db)
                db.session.commit()
                flash('User added!', category='success')
                return redirect(url_for('views.add_members'))
            else:
                flash('name does not exist', category='error')
        else:
            flash('Group created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('add_members.html', url=urllib.parse.urlparse(request.url))
