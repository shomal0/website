import urllib.parse
from .models import Group, Note
from . import db
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
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

    return render_template('home.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
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
        flash('Group created!', category='success')
        return redirect(url_for('views.home'))
    return render_template('new_group.html', url=urllib.parse.urlparse(request.url))
