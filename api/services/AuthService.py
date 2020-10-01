import jwt
import datetime
from flask import request
from flask_restful import Api
from models.models import user_schema,  User as u

secret = "\xf6\xae<Y\xde\xed\xba\x92\x97\xcd\x8bN1\t\x12?\x97\x04\xaaE\xaa\xa0m\\"

def authenticate(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return 'No token provided.', 400

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return 'Bearer token malformed.', 401

        try:
            payload = jwt.decode(token, secret)
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.', 401
            # return Api.abort(401)
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.', 401
            # return Api.abort(401)

    return wrapper

def login(username: str, password: str) -> str:
    db_user = u.query.filter_by(username=username).first()

    if not db_user:
        raise InvalidUserException('Invalid user')

    is_login_valid = db_user.check_password(password)
    if is_login_valid:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds = 30),
            "iat": datetime.datetime.utcnow(),
            "sub": user_schema.dump(db_user)['id']
        }
        
        return jwt.encode(payload, secret)
    else:
        raise InvalidPasswordException('Invalid password')

# def decode_auth_token(auth_token):
#     try:
#         payload = jwt.decode(auth_token, secret)
#         return True
#     except jwt.ExpiredSignatureError:
#         return 'Signature expired. Please log in again.'
#     except jwt.InvalidTokenError:
#         return 'Invalid token. Please log in again.'

class Error(Exception):
    message: str
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return(repr(self.message)) 

class InvalidUserException(Error):
    pass

class InvalidPasswordException(Error):
    pass
    