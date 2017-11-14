import json
import pdb
from flask import Flask, request
import datetime

from bson import Binary, Code
from bson.json_util import dumps

# 1 -
from pymongo import MongoClient

app = Flask(__name__)
# Flask auto updates any changes with this code
app.config['DEBUG'] = True


# 2 - Pass in hostname and port
mongo = MongoClient('localhost', 27017)


# 3 - specify the database
app.db = mongo.test


@app.route('/')
def my_hello():
    json_hello = 'Hello Make School!'
    return (json_hello, 200, None)


@app.route('/users')
def get_users():

    #1 get URL params
    name = request.args.get('name')

    #2 Our users collection
    users_collection = app.db.users

    #3 Find one document in our users collections
    result = users_collection.find_one(
        {'name': name}
    )

    #4 Covert result to json, its initially a python dict
    json_result = dumps(result)

    #4.b Add a break point
    # pdb.set_trace()
    #5 Return the json as part of the response body
    # param1 data, param2 result, param3 headers
    return (json_result, 200, None)


@app.route('/my_page')
def my_page_route():
    me = {'name': 'Phyllis', 'age': 100, 'hobby': 'snowboarding'}
    json_me = json.dumps(me)
    # pdb.set_trace()
    return (json_me, 200, None)


@app.route('/pets')
def fav_pets():
    pdb.set_trace()
    pets = [
        {
            'name': 'Boba',
            'breed': 'Dachshund',
            'color': 'red'
        },
        {
            'name': 'Princess',
            'breed': 'Pitbull',
            'color': 'black'
        },
        {
            'name': 'Qui Qui',
            'breed': 'House Cat',
            'color': 'Grey Stripped'
        },
        {
            'name': 'Kitty',
            'breed': 'Chihuahua',
            'color': 'Brown'
        }
    ]

    json_pets = json.dumps(pets)
    return (json_pets, 200, None)


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
