from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from db import db
from ma import ma
from resources.Unit import UnitListResource, UnitResource
from resources.Recipe import RecipeListResource, RecipeResource
from resources.Ingredient import IngredientListResource, IngredientResource

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db:3306/order_planner'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3307/order_planner'

    db.init_app(app)
    ma.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)

    api.add_resource(UnitListResource, '/unit')
    api.add_resource(UnitResource, '/unit/<unit_id>')

    api.add_resource(RecipeListResource, '/recipe')
    api.add_resource(RecipeResource, '/recipe/<recipe_id>')

    api.add_resource(IngredientListResource, '/ingredient')
    api.add_resource(IngredientResource, '/ingredient/<ingredient_id>')

    return app