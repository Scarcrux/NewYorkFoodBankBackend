from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from resources.organization import Organizations, AddOrganization, EditOrganization, AllOrganization
from resources.user import AddUser, UserLogin, UserLogout
from resources.confirmation import Confirmation, ConfirmationByUser
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkeys'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]
db = SQLAlchemy(app)
Migrate(app,db)
api = Api(app)
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

api.add_resource(Organizations,'/organization/<string:organization_name>')
api.add_resource(AddOrganization,'/add')
api.add_resource(EditOrganization,'/edit')
api.add_resource(AllOrganization,'/allorganizations')
api.add_resource(AddUser,'/register')
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
