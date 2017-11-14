from flask import Flask, jsonify, request, make_response
import pdb
import json
from bson.json_util import dumps
from util import JSONEncoder
from flask_restful import Resource, Api

# 1 - pymongo is a MongoAPI
from flask_pymongo import PyMongo
from pymongo import MongoClient
app = Flask(__name__)
app.config['DEBUG'] = True


mongo = MongoClient('localhost', 27017)
app.db = mongo.test


class User(Resource):
    def post(self):
        a_user = request.json
        users_collection = app.db.users
        result = users_collection.insert_one(a_user)
        # pdb.set_trace()
        return (a_user, 200, None)

    def get(self):
        # pdb.set_trace()
        users_collection = app.db.users
        name = request.args.get('name')

        user = users_collection.find_one({'name': name})
        # pdb.set_trace()
        return (user, 200, None)

    def put(self):
        a_user = request.json
        name = request.args.get('name')
        users_collection = app.db.users
        result = users_collection.find_one_and_replace(
            {'name': name},
            a_user)
        return (a_user, 200, None)

    def patch(self):
        a_user_fav_foods = request.json
        name = request.args.get('name')
        users_collection = app.db.users
        result = users_collection.find_one_and_update(
            {'name': name},
            {'$set': {'fav_foods': a_user_fav_foods} }
        )

        return (result, 200, None)

api = Api(app)
api.add_resource(User, '/users')

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp

if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
