from . import db
from flask_login import UserMixin

user_group = db.Table('user_group',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
                      )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    participants = db.relationship('Group', secondary=user_group, backref='participant')

    def __repr__(self):
        return f'<User: {self.name}>'


class Group(db.Model):
    name = db.Column(db.String(50), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<Group: {self.name}>'
