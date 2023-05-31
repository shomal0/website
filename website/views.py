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
    username = User.query.filter_by(name=current_user.name).first()
    return render_template('home.html', url=urllib.parse.urlparse(request.url), groups=username.groups)


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
            note_group_index = int(request.args["group_index"])
            note_group_id = current_user.groups[note_group_index].id
            new_note = Note(data=note, group_id=note_group_id)
            db.session.add(new_note)
            db.session.commit()
            flash('text sent!', category='success')
    return render_template('group.html', url=urllib.parse.urlparse(request.url), groups=current_user.groups)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    delete_data = json.loads(request.data)
    note_id = delete_data['note_id']
    note_group_index = int(delete_data['group_index'])

    note = Note.query.get(note_id)
    note_group = current_user.groups[note_group_index]
    if note:
        if note.group_id == note_group.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/about')
def about():
    return render_template('about.html', url=urllib.parse.urlparse(request.url))


@views.route('/new_group', methods=['POST', 'GET'])
@login_required
def new_group():
    if request.method == 'POST':
        group_name = request.form.get('Group_Name')
        create_group = Group(name=group_name)
        db.session.add(create_group)
        db.session.commit()
        session['group_id'] = create_group.id
        session['group_name'] = group_name
        return redirect(url_for('views.add_members'))
    return render_template('new_group.html', url=urllib.parse.urlparse(request.url))


@views.route('/add_members', methods=['POST', 'GET'])
@login_required
def add_members():
    group_name = session['group_name']
    db_group = Group.query.filter_by(name=group_name).first()
    if request.method == 'POST':
        if request.form['submit_button'] == 'add_user':
            email = request.form.get('email')
            email_in_db = User.query.filter_by(email=email).first()
            if email_in_db:
                group_name = session['group_name']
                db_group = Group.query.filter_by(name=group_name).first()
                email_in_db.groups.append(db_group)
                db.session.add(email_in_db)
                db.session.commit()
                flash('User added!', category='success')
                return redirect(url_for('views.add_members'))
            else:
                flash('email does not exist', category='error')
        else:
            flash('Group created!', category='success')
            return redirect(url_for('views.home'))
    you = User.query.filter_by(email=current_user.email).first()
    you.groups.append(db_group)
    db.session.add(you)
    db.session.commit()
    group_id = session['group_id']
    group_by_id = Group.query.filter_by(id=group_id).first()
    return render_template('add_members.html', url=urllib.parse.urlparse(request.url), members=group_by_id.members, group_name=group_name)
