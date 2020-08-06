from flask import request
from flask_restful import Resource
from models.models import Unit
from models.models import unit_schema
from db import db

class UnitListResource(Resource):
    def get(self):
        return unit_schema.dump(Unit.query.all(), many=True), 200
    
    def post(self):
        name = request.json['name']
        unit = Unit(name=name)

        db.session.add(unit) 
        db.session.commit()

        return unit_schema.dump(unit), 201

    def delete(self):
        unitId = request.json['unitIds']

        for unitId in unitIds:
            unit = Unit.query.get(unitId)

            db.session.delete(unit)
            db.session.commit()

        return 'ok', 201


class UnitResource(Resource):
    def get(self, unit_id):
        unit = Unit.query.get(unit_id)
        if not unit:
            return 'Not found', 404

        return unit_schema.dump(unit), 200
    
    def put(self, unit_id):
        unit = Unit.query.get(unit_id)

        unit.name = request.json['name']

        db.session.commit()

        return unit_schema.dump(unit), 201

    def delete(self, unit_id):
        unit = Unit.query.get(unit_id)

        db.session.delete(unit)
        db.session.commit()

        return 'ok', 201
