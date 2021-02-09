from flask_restful import Resource
import traceback
from time import time
from db import db

from models.confirmation import Confirmation
from models.user import User
from libs.mailgun import MailGunException

class Confirmation(Resource):
    # returns the confirmation page
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = Confirmation.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": "confirmation_not_found"}, 404

        if confirmation.expired:
            return {"message": "confirmation_link_expired"}, 400

        if confirmation.confirmed:
            return {"message": "confirmation_already_confirmed"}, 400

        confirmation.confirmed = True
        db.session.commit()
        return confirmation.json()


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        """
        This endpoint is used for testing and viewing Confirmation models and should not be exposed to public.
        """
        user = User.find_by_id(user_id)
        if not user:
            return {"message": "user_not_found"}, 404
        return (
            {
                "current_time": int(time()),
                # we filter the result by expiration time in descending order for convenience
                "confirmation": [
                    each.json()
                    for each in user.confirmation.order_by(Confirmation.expire_at)
                ],
            },
            200,
        )

    @classmethod
    def post(cls, user_id):
        """
        This endpoint resend the confirmation email with a new confirmation model. It will force the current
        confirmation model to expire so that there is only one valid link at once.
        """
        user = User.find_by_id(user_id)
        if not user:
            return {"message": "user_not_found"}, 404

        try:
            # find the most current confirmation for the user
            confirmation = user.most_recent_confirmation  # using property decorator
            if confirmation:
                if confirmation.confirmed:
                    return {"message": "confirmation_already_confirmed"}, 400
                confirmation.force_to_expire()

            new_confirmation = Confirmation(user_id)  # create a new confirmation
            db.session.add(new_confirmation)
            db.session.commit()
            # Does `user` object know the new confirmation by now? Yes.
            # An excellent example where lazy='dynamic' comes into use.
            user.send_confirmation_email()  # re-send the confirmation email
            return {"message": "confirmation_resend_successful"}, 201
        except MailGunException as e:
            return {"message": str(e)}, 500
        except:
            traceback.print_exc()
            return {"message": "confirmation_resend_fail"}, 500
