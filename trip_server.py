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
app.db = mongo.local


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
        email = request.args.get('email')

        if request.args.get('email'):
            user = users_collection.find_one({'email': email})

            return (user, 200, None)
        else:
            return ({"BAD REQUEST": "nahhhhh"}, 404, None)
        # pdb.set_trace()


    def put(self):
        a_user = request.json
        email = request.args.get('email')
        users_collection = app.db.users
        if request.args.get('email'):
            user = users_collection.find_one_and_replace(
                {'email': email}, email)
            return (user, 200, None)
        else:
            return ({"BAD REQUEST": "nahhhhh"}, 404, None)


    # Future feature work on this later
    def patch(self):
        a_user = request.json
        name = request.args.get('name')
        users_collection = app.db.users
        result = users_collection.find_one_and_update(
            {'name': name},
            {'$set': {'departDate': a_user_fav_foods} }
        )

        return (result, 200, None)

    # Deletes a user
    def delete(self):
        a_user = request.json
        name = request.args.get('name')
        users_collection = app.db.users
        result = users_collection.find_one_and_delete(
            {'name': name}

        )
        return (a_user, 200, None)


class Trip(Resource):
    def post(self):
        '''Create a new trip, store in the database.'''
        a_trip = request.json
        trips_collection = app.db.trips
        result = trips_collection.insert_one(a_trip)
        # pdb.set_trace()
        return (a_trip, 200, None)

    def get(self):
        '''Return a trip from the database.'''
        # pdb.set_trace()
        trips_collection = app.db.users
        location = request.args.get('location')

        if request.args.get('email'):
            trip = users_collection.find_one({'location': location})

            return (user, 200, None)
        else:
            return ({"BAD REQUEST": "nahhhhh"}, 404, None)
        # pdb.set_trace()

    def put(self):
        '''Replace a trip with a new trip.'''
        pass

    def patch(self):
        '''Replace a detail of a trip.'''
        pass

    ''' add get request to find trip '''
    ''' add data model for trips  '''
api = Api(app)
api.add_resource(User, '/users')
api.add_resource(Trip, '/trips')

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp

if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
