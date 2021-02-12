from models.confirmation import ConfirmationModel
from models.user import User
from flask import request
from flask_restful import Resource
from app import db
from flask_jwt_extended import ( create_access_token, jwt_required, get_raw_jwt )
from libs.mailgun import MailGunException
from blacklist import BLACKLIST

class AddUser(Resource):
    def post(self):
        args=request.get_json(force=True)
        username = args['username']
        password = args['password']
        email = args['email']
        user = User(username = username, password=password, email=email)
        try:
            db.session.add(user)
            db.session.commit()
            confirmation = ConfirmationModel(user.id)
            db.session.add(confirmation)
            db.session.commit()
            user.send_confirmation_email()
            return user.json()
        except MailGunException as e:
            return {"message": str(e)}, 500

class UserLogin(Resource):
    def post(self):
        args=request.get_json(force=True)
        username = args['username']
        password = args['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            confirmation = user.most_recent_confirmation()
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(identity=user.id)
                return {"access_token": access_token}, 200
            return {"message": "user_not_confirmed" }, 400

        return {"message": "user_invalid_credentials" }, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "user_logged_out"}, 200


 