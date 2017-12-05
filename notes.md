## Authentication
User creates account by entering email and password

Backend

HTTP basic protocol as a way to transfer basic information from the client to the server.
Client side sending credentials
combining the name and pw into a colon string.
convert to base64 and prepend the word "Basic"
In our postman or paw, we include the basic auth token as a header value

Setting up in iOS:
Server will fetch the user by name, and then check if the password matches the password.
Hashing a password is a one way functionality to turn a plain text password to fixed length.
We use bcrypt as a library to convert the the hashing passwords to encrypted password.
Grab the password from the parameters, convert before sending to the database

Log in:
login = bcrypt.checkpw('password'.encode('utf-8'), hashed) // returns a bool

WARNING!!! Even though we use email for username, Flask always calls it username:
request.authorization.username

## Authentication Options

JSON Web Tokens
HTTP Basic Auth
OAuth
Authentication Tokens

## Encode to http basic Auth Steps

1. Combine the username and password with a single colon.
1. (Character Encoding - UTF-8) - some users might be typing their email in another language
1. encode to base64 from utf8 - changing to a standard format (not for security)
1. Prepend the authorization method with the string "Basic"

## General Account Creating


## Decorators

Wrap auth methods in a method - called decorator
before a user can get their account - they have to hash the password


### Deployment
1. Create an account on mlab
1. Create a user on mlab
1. On Mongodb Compass enter the port copied from the mlab page
1. Enter the Hostname
1. enter the port
1. Authentication username / password Add the user and password
1. Authentication Database is the name of the database
