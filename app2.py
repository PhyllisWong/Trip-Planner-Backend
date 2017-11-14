from flask import Flask, request
import pdb
import json
from bson.json_util import dumps
from util import JSONEncoder


"""
e. Handle a get request to courses that looks for a course number from the url
parameter, returns a 400 error if the course number parameter doesn't exit, and
uses the course number to search our database courses collection for a document
with the specified course number. Return a 200 and the course if its found.

e. Handle a get request to *courses* route that fetches and returns to the user
all the courses in the database.

f. Create another route called count_courses that returns the number of course documents in our database."""


# 1 - pymongo is a MongoAPI
from pymongo import MongoClient
app = Flask(__name__)
app.config['DEBUG'] = True

# 2 - Pass in hostname and port
mongo = MongoClient('localhost', 27017)

# 3 - specify the database
app.db = mongo.test


@app.route('/person')
def person_route():
    # pdb.set_trace()

    person = {"name": "Phyllis", "age": 100}
    json_person = json.dumps(person)
    return (json_person, 200, None)


@app.route('/pets', methods=['GET', 'POST'])
def add_pets():
    if request.method == 'POST':
        pdb.set_trace()
        json_pets = json.dumps(request.json)
        return (json_pets, 201, None)


@app.route('/courses', methods=['POST'])
def post_courses():
    # 1 get body from post request
    a_course = request.json

    # 2 Our courses collection
    courses_collection = app.db.courses

    # 3 insert a_course into course collection
    # Inserting one user into our users collection
    result = courses_collection.insert_one(
        a_course
    )
    pdb.set_trace()

    # 4 if insert was succesful, return 200 and the a_course back to requester
    # 4 Covert result to json, its initially a python dict
    json_representation = JSONEncoder().encode(a_course)
    # 5 Return the json as part of the response body
    # param1 data, param2 result, param3 headers
    return json_representation, 200, None


@app.route('/courses', methods=['GET'])
def get_courses():
    # 1 get URL params
    number = request.args.get('number')

    # 2 Our users collection
    courses_collection = app.db.courses

    # 3 Find one document in our users collections
    result = courses_collection.find_one(
        {'number': number}
    )

    # 4 Covert result to json, its initially a python dict
    json_result = JSONEncoder().encode(number)

    # 4.b Add a break point
    # pdb.set_trace()
    # 5 Return the json as part of the response body
    # param1 data, param2 result, param3 headers
    return (json_result, 200, None)


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
