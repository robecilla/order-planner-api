from flask import request
from flask_restful import Resource
from models.models import Ingredient
from models.models import ingredient_schema
from services.AuthService import authenticate
from db import db

class IngredientListResource(Resource):
    method_decorators = [authenticate]

    def get(self):
        return ingredient_schema.dump(Ingredient.query.all(), many=True), 200
    
    def post(self):
        name = request.json['name']
        ingredient = Ingredient(name=name)

        db.session.add(ingredient) 
        db.session.commit()

        return ingredient_schema.dump(ingredient), 201

    def delete(self):
        ingredient_ids = request.json['ingredient_ids']

        for ingredient_id in ingredient_ids:
            ingredient = Ingredient.query.get(ingredient_id)

            db.session.delete(ingredient)
            db.session.commit()

        return 'ok', 201


class IngredientResource(Resource):
    method_decorators = [authenticate]
    
    def get(self, ingredient_id):
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return 'Not found', 404

        return ingredient_schema.dump(ingredient), 200
    
    def put(self, ingredient_id):
        ingredient = Ingredient.query.get(ingredient_id)

        ingredient.name = request.json['name']
        ingredient.quantity = request.json['quantity']
        ingredient.unit = request.json['unit_id']

        db.session.commit()

        return ingredient_schema.dump(ingredient), 200

    def delete(self, ingredient_id):
        ingredient = Ingredient.query.get(ingredient_id)

        db.session.delete(ingredient)
        db.session.commit()

        return 'ok', 201
