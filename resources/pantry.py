from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.pantry import Pantry
from flask import request, jsonify
from app import db,ma

class PantrySchema(ma.Schema):
    class Meta:
        fields = ('id','pantry_name','type','address','contact_name','phone','hours','geocode')

pantry_schema = PantrySchema()
pantries_schema = PantrySchema(many=True)
class Pantries(Resource):
    def get(self,pantry_name):
        pantry = Pantry.query.filter_by(pantry_name=pantry_name).first()
        if pantry:
            return pantry.json()
        else:
            return {'name':None},404
    @jwt_required
    def delete(self,pantry_name):
        Pantry.query.filter_by(pantry_name = pantry_name).delete()
        db.session.commit()
        return {'note':'delete success'}

class AddPantry(Resource):
    @jwt_required
    def post(self):
        args=request.get_json(force=True)
        pantry_name = args['pantry_name']
        contact_name = args['contact_name']
        phone = args['phone']
        type = args['type']
        address = args['address']
        geocode = args['geocode']
        hours = args['hours']
        organization_id = args['organization_id']
        pantry = Pantry(pantry_name = pantry_name, contact_name = contact_name, phone = phone, type = type,
        address = address, geocode = geocode, hours = hours, organization_id=organization_id)
        db.session.add(pantry)
        db.session.commit()
        return pantry.json()

class EditPantry(Resource):
    @jwt_required
    def put(self):
        args=request.get_json(force=True)
        pantry_id = args['id']
        pantry_name = args['pantry_name']
        contact_name = args['contact_name']
        phone = args['phone']
        type = args['type']
        address = args['address']
        geocode = args['geocode']
        hours = args['hours']
        pantry = Pantry.query.filter_by(id=pantry_id).first()
        pantry.pantry_name = pantry_name
        pantry.contact_name = contact_name
        pantry.phone = phone
        pantry.type = type
        pantry.address = address
        pantry.geocode = geocode
        pantry.hours = hours
        db.session.commit()
        return pantry.json()

class AllPantries(Resource):
    def get(self):
        shares = db.session.query(Pantry)
        result = pantries_schema.dump(shares)
        return jsonify(result)

class MyPantries(Resource):
    def get(self, organization_id):
        shares = db.session.query(Pantry).filter_by(organization_id = organization_id)
        result = pantries_schema.dump(shares)
        return jsonify(result)

class SinglePantry(Resource):
    def get(self, pantry_id):
        shares = db.session.query(Pantry).filter_by(id = pantry_id)
        result = pantries_schema.dump(shares)
        return jsonify(result)
