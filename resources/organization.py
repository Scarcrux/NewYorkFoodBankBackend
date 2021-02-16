from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.organization import Organization
from flask import request
from app import db

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
        contact_name = args['contact_name']
        phone = args['phone']
        type = args['type']
        address = args['address']
        geocode = args['geocode']
        hours = args['hours']
        user_id = args['user_id']
        organization = Organization(organization_name = organization_name, contact_name = contact_name, phone = phone, type = type,
        address = address, geocode = geocode, hours = hours, user_id=user_id)
        db.session.add(organization)
        db.session.commit()
        return organization.json()

class EditOrganization(Resource):
    @jwt_required
    def put(self):
        args=request.get_json(force=True)
        organization_id = args['id']
        organization_name = args['organization_name']
        contact_name = args['contact_name']
        phone = args['phone']
        type = args['type']
        address = args['address']
        geocode = args['geocode']
        hours = args['hours']
        organization = Organization.query.filter_by(id=organization_id).first()
        organization.organization_name = organization_name
        organization.contact_name = contact_name
        organization.phone = phone
        organization.type = type
        organization.address = address
        organization.geocode = geocode
        organization.hours = hours
        db.session.commit()
        return organization.json()

class AllOrganization(Resource):
    def get(self):
        allorganizations=Organization.query.filter_by(organization_name = organization_name)
        return [organization.json() for organization in allorganizations ]

class MyOrganization(Resource):
    def get(self):
        args=request.get_json(force=True)
        user_id = args['user_id']
        allorganizations=Organization.query.filter_by(user_id = user_id)
        return [organization.json() for organization in allorganizations ]
