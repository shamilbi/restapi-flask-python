# coding: utf-8

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import Item as ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    # class variable
    parser.add_argument('price', type=float, required=True,
                        help='price must be filled')
    parser.add_argument('store_id', type=int, required=True,
                        help='store_id must be filled')
    # other keys from json will be skipped

    @jwt_required()
    def get(self, name):
        '''
        /auth --> access_token
        /item/name
            Authorization: "JWT $access_token"
        '''
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    def post(self, name):
        'create'
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': 'item "{}" already exists'.format(name)}, 400
            # bad request
        data = Item.parser.parse_args()
        try:
            item = ItemModel(name, data['price'], data['store_id'])
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'}, 500
            # internal server error
        return item.json(), 201
        # created
        # 202 - accepted (delaying of creation)

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        'create or update, idempotent operation: F*F = F'
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class Items(Resource):
    def get(self):
        #items = ItemsModel()
        return {'items': [i.json() for i in ItemModel.query.all()]}
