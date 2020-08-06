import json
from flask import request
from flask_restful import Resource
from sqlalchemy.orm import joinedload
from models.models import Ingredient, Recipe, recipe_schema
from models.models import Measure
from db import db

class RecipeListResource(Resource):
    def get(self):
        recipes = Recipe.query.all()
        return recipe_schema.dump(recipes, many=True), 200
    
    def post(self):
        recipe_name = request.get_json()['name']
        recipe = Recipe(name=recipe_name)

        ingredients = request.get_json()['ingredients']

        for ingredient in ingredients: 
            measure = Measure(quantity=ingredient['quantity'], ingredient_id=ingredient['ingredient_id'], unit_id=ingredient['unit_id'])
            recipe.measures.append(measure)

        db.session.add(recipe) 
        db.session.commit()

        return recipe_schema.dump(recipe), 201


class RecipeResource(Resource):
    def get(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)

        if not recipe:
            return 'Not found', 404

        return recipe_schema.dump(recipe), 200
    
    def put(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)

        measures = request.get_json()['measures']
        operation = request.get_json()['operation']

        for measure in measures:
            if operation == 'add':
                m = Measure(quantity=measure['quantity'], ingredient_id=measure['id'], unit_id=measure['unitId'])
                recipe.measures.append(m)
            elif operation == 'delete':
                m = Measure.query.get(measure)
                recipe.measures.remove(m)
                db.session.delete(m)
            else:
                pass


        db.session.commit()

        return recipe_schema.dump(recipe), 200

    def delete(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)
        measure = Measure.query.join(Measure, Recipe.measures).filter(Recipe.id == recipe_id).first()

        db.session.delete(measure)
        db.session.delete(recipe)
        db.session.commit()

        return "ok", 201
