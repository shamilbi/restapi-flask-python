# coding: utf-8

from flask_restful import Resource, reqparse
from models.user import User


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    # class variable
    parser.add_argument('username', type=str, required=True,
                        help='username must be filled')
    parser.add_argument('password', type=str, required=True,
                        help='password must be filled')
    # other keys from json will be skipped

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400
        user = User(data['username'], data['password'])
        user.save_to_db()
        return {'message': 'User created successfully'}, 201
