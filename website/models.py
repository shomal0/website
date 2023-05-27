from datetime import datetime
from flask_login import UserMixin

from . import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


user_group = db.Table('user_group',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
                      )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    groups = db.relationship('Group', secondary=user_group, backref='members')

    def __repr__(self):
        return f'<User: {self.name}>'


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    notes = db.relationship('Note')

    def __repr__(self):
        return f'<Group: {self.name}>'
