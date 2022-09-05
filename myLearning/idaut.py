from functools import wraps
from flask import Flask, request, jsonify, abort

def get_token_auth_header():
    # check if authorization is not in request
    if 'Authorization' not in request.headers:
        abort(401)
    # get the token
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')
    #check if token is valid
    if len(header_parts) != 2:
        abort(401)
    return header_parts[1]

def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt = get_token_auth_header()
        return f(jwt, *args, **kwargs)
    return wrapper

app = Flask(__name__)

@app.route('/headers')
@requires_auth
def headers(jwt):
    print(jwt)
    return "not implemented"