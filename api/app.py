from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from db import db
from ma import ma
from resources.Unit import UnitListResource, UnitResource
from resources.Recipe import RecipeListResource, RecipeResource
from resources.Ingredient import IngredientListResource, IngredientResource
from resources.User import UserListResource, UserResource
from services.AuthService import login, InvalidUserException, InvalidPasswordException

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

    api.add_resource(UserListResource, '/user')
    api.add_resource(UserResource, '/user/<user_id>')

    # authentication route/path/endpoint
    @app.route('/login', methods=['POST'])
    def login_route():
        request_data = request.get_json()
        username = request_data['username']        
        password = request_data['password']

        try:
            return login(username, password)
        except InvalidUserException as exception:
            return exception.message, 404
        except InvalidPasswordException as exception:
            return exception.message, 401
                

    return app