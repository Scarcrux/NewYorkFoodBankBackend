from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import ( JWTManager, jwt_required )
from flask_sqlalchemy import SQLAlchemy
from blacklist import BLACKLIST
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_talisman import Talisman

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkeys'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]

db = SQLAlchemy(app)
Migrate(app,db)
api = Api(app)
jwt = JWTManager(app)
ma = Marshmallow(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

# content security policy
csp = {
    'connect-src': 'https://nyfoodbank.herokuapp.com/',
    'default-src': '\'self\'',
    'img-src': '*',
    'media-src': [
        '*'
    ],
    'script-src': '*',
    'worker-src': '*'
}
talisman = Talisman(app, content_security_policy=csp)

from resources.organization import Organizations, AddOrganization, EditOrganization, AllOrganization, MyOrganization, AnOrganization
from resources.user import AddUser, UserLogin, UserLogout
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.pantry import Pantries, AddPantry, EditPantry, AllPantries, MyPantries, SinglePantry
from resources.payment import Payment

api.add_resource(Organizations,'/organization/<string:organization_name>')
api.add_resource(AddOrganization,'/add')
api.add_resource(EditOrganization,'/edit')
api.add_resource(AllOrganization,'/allorganizations')
api.add_resource(MyOrganization,'/myorganizations/<int:user_id>')
api.add_resource(MyPantries,'/mypantries/<int:organization_id>')
api.add_resource(AnOrganization,'/org/<int:id>')
api.add_resource(Pantries,'/pantry/<string:pantry_name>')
api.add_resource(SinglePantry,'/pan/<int:pantry_id>')
api.add_resource(AddPantry,'/addPantry')
api.add_resource(EditPantry,'/editPantry')
api.add_resource(AllPantries,'/allpantries')
api.add_resource(AddUser,'/register')
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
api.add_resource(Payment, "/pay")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True)
