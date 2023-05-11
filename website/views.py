import json
import urllib.parse
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.json import jsonify
from flask_login import login_required, current_user

from . import db
from .models import Group, Note

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
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

    return render_template('home.html', user=current_user,  url=urllib.parse.urlparse(request.url))


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
        name = request.form.get('Group_Name')
        create_group = Group(name=name)
        db.session.add(create_group)
        db.session.commit()
        flash('Group created!', category='success')
        return redirect(url_for('views.home'))
    return render_template('new_group.html', url=urllib.parse.urlparse(request.url))
