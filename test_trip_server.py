import trip_server
import unittest
import json
from pymongo import MongoClient
from flask_restful import Resource, Api
db = None


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = trip_server.app.test_client()

        # Run app in testing mode to retrieve exceptions and stack traces
        trip_server.app.config['TESTING'] = True

        # Inject test database into application
        mongo = MongoClient('localhost', 27017)
        global db
        db = mongo.test_database
        trip_server.app.db = db

        ## We do this to clear our database before each test runs
        db.drop_collection('users')

    def test_getting_a_user(self):
        ## 2 Post user to database to test GET request
        self.app.post('/users',
                          headers=None,
                          data=json.dumps(dict(
                              name="Chris Mauldin",
                              email="chris@example.com"
                          ) ),
                          content_type='application/json')

        ## 3 Make a get request to fetch the posted user

        response = self.app.get('/users',
                                query_string=dict(email="chris@example.com") )

        # Decode reponse
        response_json = json.loads(response.data.decode() )

        ## Test to see if GET request was succesful
        ## Here we check the status code
        self.assertEqual(response.status_code, 200)

    # Test a PUT request
    def test_update_a_user(self):

        self.app.post('/users',
                          headers=None,
                          data=json.dumps(dict(
                              name="Phyllis Wong",
                              email="Phyllis@example.com"
                          ) ),
                          content_type='application/json')

        self.app.put('/users',
                        headers=None,
                        data=json.dumps(dict(
                            name="Phyllis Smith",
                            email="Phyllis@gmail.com"
                        ) ),
                        content_type='application/json')

        response = self.app.get('/users',
                                query_string=dict(email="Phyllis@gmail.com") )

        response_json = json.loads(response.data.decode() )

        ## Test to see if PUT request was succesful
        ## Here we check the status code
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
