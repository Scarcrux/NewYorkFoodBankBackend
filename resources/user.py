from models.confirmation import Confirmation
from models.user import User
from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from db import db
from libs.mailgun import MailGunException

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
            confirmation = Confirmation(user.id)
            user.send_confirmation_email()
            db.session.add(confirmation)
            db.session.commit()
            return user.json()
        except MailGunException as e:
            return {"message": str(e)}, 500
       



class UserLogin(Resource):
    def post(self):
        args=request.get_json(force=True)
        username = args['username']
        password = args['password']
        user = UserModel.find_by_username(username=username)

        if user and user.check_password(user.password, password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(user.id, fresh=True)
                return (
                    {"access_token": access_token},
                    200,
                )
            return {"message": "user_not_confirmed" }, 400

        return {"message": "user_invalid_credentials" }, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": "user_logged_out"}, 200


