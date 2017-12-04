from flask import Flask, jsonify, request, make_response, g
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from pymongo import MongoClient
from basicauth import decode # does not work yet!!!!
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson import BSON
from util import JSONEncoder
import pdb
import json
import sys


import bcrypt

# 1 - pymongo is a MongoAPI
app = Flask(__name__)
app.config['DEBUG'] = True


# Deployed database
# mongo = MongoClient('mongodb://phyllisWong:test@ds139909.mlab.com:39909/trip_planner_pro')

# Local database
mongo = MongoClient('mongodb://localhost:27017/')
app.db = mongo.trip_planner_pro
app.bcrypt_rounds = 5

def validate_auth(user, password):
    users_collection = app.db.users
    user = users_collection.find_one({'username': user})
    # pdb.set_trace()
    if user is None:
        # pdb.set_trace()
        return False
    else:
        # pdb.set_trace()
        encoded_password = password.encode('utf-8')
        if bcrypt.hashpw(encoded_password, user['password']) == user['password']:
            # pdb.set_trace()
            # g.setdefault('user', user)
            return True
        else:
            return False

# Authentication decorator
def authenticated_request(func):
    def wrapper(*args, **kwargs):
        auth = request.authorization

        if not auth or not validate_auth(auth.username, auth.password):
            # pdb.set_trace()
            return ({'error': 'Basic Authorization Required'}, 401, None)

        return func(*args, **kwargs)

    return wrapper


class User(Resource):

    def __init__(self):
        self.users_collection = app.db.users

    def post(self):
        json_body = request.json
        password = json_body['password']
        email = json_body['email']

        # check if the user already exists in the database
        check_for_user = self.users_collection.find_one({'email': email})
        if check_for_user is not None:
            return ({'error': 'User already exists'}, 409, None)
        # if the email doesn't exist
        else:
            encoded_password = password.encode('utf-8')
            hashed = bcrypt.hashpw(encoded_password, bcrypt.gensalt(app.bcrypt_rounds))
            # hashed = hashed.decode()
            # pdb.set_trace()

            json_body['password'] = hashed

            result = self.users_collection.insert_one(json_body)
            user = self.users_collection.find_one({"_id": result.inserted_id})
            return ({'Success':'A new user was added'}, 200, None)

    @authenticated_request
    def get(self):
        # user = g.get('user', None)
        # user.pop('password')
        username = request.authorization.username
        user = self.users_collection.find_one({'username': username})
        # pdb.set_trace()
        return ({'Success':'A user was found'}, 200, None)

    @authenticated_request
    def put(self):
        username = request.authorization.username
        json_body = request.json
        password = json_body['password']
        email = json_body['email']

        check_for_user = self.users_collection.find_one({'email': email})
        if check_for_user is not None:
            check_for_user.find_one_and_replace(
                {'email': email}, email)
            return ({'success': 'user has been replaced'}, 200, None)
        else:
            return ({'error': 'BAD REQUEST'}, 404, None)

    @authenticated_request
    def patch(self):
        username = request.authorization.username
        new_user = request.json['new_username']

        user = self.users_collection.find_one_and_update(
            {'user': username},
            {'$set': {'user': new_user} },
            return_document=ReturnDocument.AFTER
        )
        return ({'succesful': 'user has been updated'}, 200, None)

    @authenticated_request
    def delete(self):
        username = request.authorization.username
        self.users_collection.remove({'user': username})
        return ({'success': 'user had been deleted'}, 200, None)

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
        pdb.set_trace()
        trips_collection = app.db.trips
        destination = request.args.get('destination')

        if request.args.get('destination'):
            trip = trips_collection.find_one({'destination': destination})

            return (trip, 200, None)
        else:
            return ({"BAD REQUEST"}, 404, None)
        # pdb.set_trace()

    def put(self):
        '''Replace a trip with a new trip.'''
        a_trip = request.json
        destination = request.args.get('destination')
        trips_collection = app.db.trips
        if request.args.get('destination'):
            trip = users_collection.find_one_and_replace(
                {'destination': destination}, destination)
            return (trip, 200, None)
        else:
            return ({"BAD REQUEST"}, 404, None)
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
