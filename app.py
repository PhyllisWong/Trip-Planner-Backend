from flask import Flask, jsonify, request, make_response, g
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from pymongo import MongoClient
from basicauth import decode # does not work yet!!!!
from bson import Binary, Code
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
mongo = MongoClient('mongodb://phyllis:test@ds123722.mlab.com:23722/trip_planner_phyllis')

# Local database
# mongo = MongoClient('mongodb://localhost:27017/')
app.db = mongo.trip_planner_phyllis
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
        # g is user variable with a {:}
        g.setdefault('user', user)
        return bcrypt.checkpw(encoded_password, user['password'])
            # pdb.set_trace()


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
            return ({'new user added': '{}'.format(user)}, 200, None)

    @authenticated_request
    def get(self):
        username = request.authorization.username
        user = self.users_collection.find_one({'username': username})
        if user is not None:
            # pdb.set_trace()
            return (user, 200, None)
        return ({'error': 'User does not exists'}, 404, None)

    @authenticated_request # Does not work yet
    def put(self):
        username = request.authorization.username
        new_user = request.json

        user = self.users_collection.find_one_and_update(
            {'user': username},
            {'$set': {'user': new_user} },
            return_document=ReturnDocument.AFTER
        )
        return ({'user was updated': '{}'.format(user)}, 200, None)

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

    def __init__(self):
        self.trips_collection = app.db.trips

    @authenticated_request
    def post(self):
        '''Create a new trip, store in the database.'''
        json_body = request.json
        # pass in the user_id
        json_body['user_id'] = g.get('user')['_id']

        trips_collection = app.db.trips

        destination = json_body['destination']
        waypoints = json_body['waypoints']
        completed = json_body['completed']

        check_for_trip = self.trips_collection.find_one({'destination': destination})
        if check_for_trip is not None:
            return ({'error': 'Trip already exists'}, 409, None)
        trip = trips_collection.insert_one(json_body)
        # pdb.set_trace()
        return ({'a new trip was added': trip}, 200, None)

    @authenticated_request
    def get(self):
        '''Return all trips from the database.'''
        # pdb.set_trace()
        user = g.get('user')['_id']

        trips = self.trips_collection.find_one({'user_id': user})
        all_trips = []
        if trips is not None:
            for trip in trips:
                all_trips += [trip]

        return (all_trips, 200, None)


            # return ("BAD REQUEST", 404, None)
        # pdb.set_trace()

        # username = request.authorization.username
        # user = self.users_collection.find_one({'username': username})
        # if user is not None:
        #     # pdb.set_trace()
        #     return ({'Success':'{}'.format(user)}, 200, None)
        # return ({'error': 'User does not exists'}, 404, None)

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
    '''Serialize output JSON data.'''
    if type(data) is dict:
        if data['password']:
            data['password'] = data['password'].decode('utf-8')
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp

if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
