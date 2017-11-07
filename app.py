import json
import pdb
from flask import Flask, request

app = Flask(__name__)
# Flask auto updates any changes with this code
app.config['DEBUG'] = True


@app.route('/')
def my_hello():
    json_hello = 'Hello Make School!'
    return (json_hello, 200, None)


@app.route('/my_page')
def my_page_route():
    me = {'name': 'Phyllis', 'age': 100, 'hobby': 'snowboarding'}
    json_me = json.dumps(me)
    # pdb.set_trace()
    return (json_me, 200, None)


@app.route('/pets')
def fav_pets():
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
        }
    ]

    json_pets = json.dumps(pets)
    return (json_pets, 200, None)


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
