# coding: utf-8

from db import db

# pylint: false positive: db.Column, ...


class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    # autoincrement
    name = db.Column(db.String(100))

    items = db.relationship('Item', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'items': [i.json() for i in self.items.all()]}

    def save_to_db(self):
        db.session.add(self)
        # insert or update
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # select ... limit 1

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
