from flask import Flask, jsonify, request, make_response, g
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from pymongo import MongoClient
from basicauth import decode
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson import BSON
from util import JSONEncoder
import json
import sys


import bcrypt

# 1 - pymongo is a MongoAPI
app = Flask(__name__)
app.config['DEBUG'] = True


mongo = MongoClient('mongodb://phyllisWong:test@ds139909.mlab.com:39909/trip_planner_pro')
app.db = mongo.trip_planner_pro
app.bcrypt_rounds = 5

# Authentication decorator
def authentication_request(func):
    # Set unlimited arguments to return back
    def wrapper(*args, **kwargs):
        auth = request.authorization
        # Gets the headers in the Authorization JSON
        auth_code = request.headers['authorization']
        # import pdb; pdb.set_trace()
        email, password = decode(auth_code)
        if email is not None and password is not None:
            users_collection = app.db.users
            found_user = users_collection.find_one({'email': email})
            if found_user is not None:
                encoded_password = password.encode('utf-8')
                if bcrypt.checkpw(encoded_password, found_user['password']):
                    return func(*args, **kwargs)
                else:
                    return ({'error': 'email or password is not correct'}, 401, None)
            else:
                return ({'error': 'email or password is not correct'}, 401, None)
        else:
            return ({'error': 'could not find user in the database'})
    return wrapper

class User(Resource):
    def post(self): # This WORKS with Paw!!!
        # Get data from the body of the http request
        json = request.json
        users_collection = app.db.users

        #Getting password from client
        password = json.get('password')
        print(password)

        # save the value of the data in a variable
        email = json["email"]
        password = json["password"]

        # check if the user already exists in the database
        check_for_user = users_collection.find_one({'email': email})

        # if the email already exists in the database
        # alert user that the email has been used
        if check_for_user is not None:
            return ('This email is already in use.', 401, None)

        # if the email doesn't exist
        # store email and encode and hash password to be saved in database
        else:
            # Encrypting password by using a hash function and salt
            encoded_password = password.encode('utf-8')

            # base64 encoding handled by the bcrypt library
            hashed = bcrypt.hashpw(
                encoded_password, bcrypt.gensalt(app.bcrypt_rounds)
                )
            password = hashed
            print("This is the json " + str(json))
            if 'username' in json and 'email' in json and 'password' in json:
                # insert user and user details to database
                user = users_collection.find_one({'email': email})
                if user is not None:
                    # User exists
                    return ({'error': 'User already exists'}, 409, None)
                users_collection.insert_one(json)
                json.pop('password')
                return ('New user has been added.', 200, None)
            else:
                return (None, 404, None)


    @authentication_request
    def get(self):
        # import pdb pdb.set_trace()
        # Get route to database
        users_collection = app.db.users
        auth = request.authorization
        # print("Current password:" + user_password)
        encoded_password = user_password.encode('utf-8')
        if auth.email is not None and auth.password is not None:
            user_find = users_collection.find_one({'email': auth.email})
            user_find.pop('password')
            return(user_find, 200, None)
        else:
            return(None, 401, None)
        # pdb.set_trace()

    def put(self):
        edit_user = request.json
        email = request.args.get('email')
        users_collection = app.db.users
        if request.args.get('email'):
            user = users_collection.find_one_and_replace(
                {'email': email}, email)
            return (user, 200, None)
        else:
            return ({"BAD REQUEST"}, 404, None)


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
