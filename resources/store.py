# coding: utf-8

from flask_restful import Resource
from models.store import Store as StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404

    def post(self, name):
        'create'
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': 'Store "{}" already exists'.format(name)}, 400
            # bad request
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured inserting the Store'}, 500
            # internal server error
        return store.json(), 201
        # created
        # 202 - accepted (delaying of creation)

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}


class Stores(Resource):
    def get(self):
        return {'stores': [i.json() for i in StoreModel.query.all()]}
