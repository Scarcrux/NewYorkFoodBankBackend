from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.organization import Organization
from flask import request, jsonify
from app import db, ma


class OrganizationSchema(ma.Schema):
    class Meta:
        fields = ('id','organization_name','type','address','phone','url','user_id')

organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)
class Organizations(Resource):
    def get(self,organization_name):
        organization = Organization.query.filter_by(organization_name=organization_name).first()
        if organization:
            return organization.json()
        else:
            return {'name':None},404
    @jwt_required
    def delete(self,organization_name):
        Organization.query.filter_by(organization_name = organization_name).delete()
        db.session.commit()
        return {'note':'delete success'}

class AddOrganization(Resource):
    @jwt_required
    def post(self):
        args=request.get_json(force=True)
        organization_name = args['organization_name']
        phone = args['phone']
        type = args['type']
        address = args['address']
        url = args['url']
        user_id = args['user_id']
        organization = Organization(organization_name = organization_name, phone = phone, type = type,
        address = address, url = url, user_id = user_id)
        db.session.add(organization)
        db.session.commit()
        return organization.json()

class EditOrganization(Resource):
    @jwt_required
    def put(self):
        args=request.get_json(force=True)
        organization_id = args['id']
        organization_name = args['organization_name']
        phone = args['phone']
        type = args['type']
        address = args['address']
        url = args['url']
        organization = Organization.query.filter_by(id=organization_id).first()
        organization.organization_name = organization_name
        organization.phone = phone
        organization.type = type
        organization.address = address
        organization.url = url
        db.session.commit()
        return organization.json()

class AllOrganization(Resource):
    def get(self):
        shares = db.session.query(Organization)
        result = organizations_schema.dump(shares)
        return jsonify(result)

class MyOrganization(Resource):
    def get(self, user_id):
        shares = db.session.query(Organization).filter_by(user_id = user_id)
        result = organizations_schema.dump(shares)
        return jsonify(result)

class AnOrganization(Resource):
    def get(self, id):
        shares = db.session.query(Organization).filter_by(id = id)
        result = organizations_schema.dump(shares)
        return jsonify(result)
