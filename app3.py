from flask import Flask, jsonify, request, make_response
import pdb
import json
from bson.json_util import dumps
from util import JSONEncoder
# from flask_restful import *
from flask_restful import Resource, Api

# 1 - pymongo is a MongoAPI
from pymongo import MongoClient
app = Flask(__name__)
app.config['DEBUG'] = True


mongo = MongoClient('localhost', 27017)
app.db = mongo.test


class User(Resource):

    def post(self):

        # data = request.get_json()
        # if not data:
        #     data = {"response": "ERROR"}
        #     return jsonify(data)
        # else:
        a_user = request.json
        users_collection = app.db.users
        result = users_collection.insert_one(a_user)
        # pdb.set_trace()
        # 4 if insert was succesful, return 200 and the a_course back to requester
        # 4 Covert result to json, its initially a python dict
        # json_results = json.dumps(result)
        # json_results = JSONEncoder().encode(a_user)
        # 5 Return the json as part of the response body
        # param1 data, param2 result, param3 headers
        return (a_user, 200, None)


    def get(self):
        # pdb.set_trace()
        users_collection = app.db.users

        name = request.args.get("name")
        user = users_collection.find_one({"name": name})

        # 4 Covert result to json, its initially a python dict
        # json_result = JSONEncoder().encode(user)
        # pdb.set_trace()
        return (a_user, 200, None)


    def put(self):
        pass

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
