from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify, request
from flask_jwt import JWT,jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)
api = Api(app)

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(80))
    contact_name = db.Column(db.String(20))
    phone = db.Column(db.String(10))
    type = db.Column(db.String(10))
    address = db.Column(db.String(80))
    hours = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def __init__(self,name):
        self.organization_name = organization_name
        self.contact_name = contact_name
        self.phone = phone
        self.type = type
        self.address = address
        self.hours = hours
    def json(self):
        return {
            'organization_name': self.organization_name,
            'contact_name': self.contact_name,
            'phone': self.phone,
            'type': self.type,
            'address': self.address,
            'hours': self.hours
        }

class Organizations(Resource):
    def get(self,organization_name):
        organization = Organization.filter_by(organization_name=organization_name).first()
        if organization:
            return organization.json()
        else:
            return {'name':None},404
    @jwt_required()
    def delete(self,organization_name):
        organization = Organization.query.filter_by(organization_name = organization_name).first()
        db.session.delete(organization)
        db.session.commit()
        return {'note':'delete success'}

class AddOrganization(Resource):
    def post(self):
        args=request.get_json(force=True)
        organization_name = args['organization_name']
        contact_name = args['contact_name']
        phone = args['phone']
        type = args['type']
        address = args['address']
        hours = args['hours']
        user_id = args['user_id']
        organization = Organization(organization_name = organization_name, contact_name = contact_name, phone = phone, type = type,
        address = address, hours = hours, user_id=user_id)
        db.session.add(organization)
        db.session.commit()
        return organization.json()

class EditOrganization(Resource):
    @jwt_required()

    def edit(self):
        args=request.get_json(force=True)
        organization_name = args['organization_name']
        contact_name = args['contact_name']
        phone = args['phone']
        type = args['type']
        address = args['address']
        hours = args['hours']
        organization = Organization.filter_by(organization_name=organization_name).first()
        organization.organization_name = organization_name
        organization.contact_name = contact_name
        organization.phone = phone
        organization.type = type
        organization.address = address
        organization.hours = hours
        db.session.commit()
        return organization.json()

class AllOrganization(Resource):
    def get(self):
        allorganizations=Organization.query.all()
        return [organization.json() for organization in allorganizations ]

class User(db.Model):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def json(self):
        return {'name':self.username,'password':self.password_hash}

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class AddUser(Resource):
    def post(self):
        args=request.get_json(force=True)
        username = args['username']
        password = args['password']
        user = User(username = username, password=password)
        db.session.add(user)
        db.session.commit()
        return user.json()

def authenticate(username,password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()

jwt = JWT(app,authenticate,identity)
api.add_resource(Organizations,'/organization/<string:name>')
api.add_resource(AddOrganization,'/add')
api.add_resource(EditOrganization,'/edit')
api.add_resource(AllOrganization,'/allorganizations')
api.add_resource(AddUser,'/register')
if __name__ == '__main__':
    app.run(debug=True)
