# coding: utf-8

from db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # autoincrement
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        # insert or update
        db.session.commit()

    @classmethod
    def by_username(cls, name):
        return cls.query.filter_by(username=name).first()

    @classmethod
    def by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()
