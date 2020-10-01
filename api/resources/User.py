from flask import request
from flask_restful import Resource
from models.models import User
from models.models import user_schema
from db import db

class UserListResource(Resource):
    def get(self):
        return user_schema.dump(User.query.all(), many=True), 200
    
    def post(self):
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']        

        user = User(username=username, email=email)

        user.set_password(password)

        db.session.add(user) 
        db.session.commit()

        return user_schema.dump(user), 201


class UserResource(Resource):
    def get(self, User_id):
        User = User.query.get(User_id)
        if not User:
            return 'Not found', 404

        return user_schema.dump(User), 200
    
    def put(self, User_id):
        User = User.query.get(User_id)

        User.name = request.json['name']

        db.session.commit()

        return user_schema.dump(User), 201

    def delete(self, User_id):
        User = User.query.get(User_id)

        db.session.delete(User)
        db.session.commit()

        return 'ok', 201
