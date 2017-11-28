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
