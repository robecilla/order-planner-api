from db import db
from ma import ma
from werkzeug.security import generate_password_hash, check_password_hash

recipe_measure = db.Table('recipe_measure',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('measure_id', db.Integer, db.ForeignKey('measure.id'), primary_key=True)
)

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

class Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)

    recipe = db.relationship('Recipe', secondary=recipe_measure, lazy='joined', backref=db.backref('measures', lazy=True))
    ingredient = db.relationship('Ingredient', lazy='joined', backref=db.backref('ingredient', lazy=True))
    unit = db.relationship('Unit', backref=db.backref('unit', uselist=False))

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
        
class UnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit

unit_schema = UnitSchema()

class IngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingredient

ingredient_schema = IngredientSchema()

class MeasureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Measure

    unit = ma.Pluck(UnitSchema, "name")
    ingredient =  ma.Nested(IngredientSchema)
    
measure_schema = MeasureSchema()

class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe

    measures = ma.Nested(MeasureSchema, many=True)

recipe_schema = RecipeSchema()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "username", "email")

user_schema = UserSchema()

