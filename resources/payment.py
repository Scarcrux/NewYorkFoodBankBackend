from stripe import error
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.payment import PaymentModel
from flask import request, jsonify
from app import db,ma
import sys, os

class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('id','amount','user_id')

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)
class Payment(Resource):
        
    def post(self, user_id):
        """
        Expect a token and a list of item ids from the request body.
        Construct an order and talk to the Strip API to make a charge.
        """
        args=request.get_json(force=True)
        amount = args['amount']
        payment = PaymentModel(amount=amount, status="pending", user_id=user_id)
        db.session.add(payment)
        db.session.commit() # this does not submit to Stripe

        try:
            payment.set_status("failed")  # assume the payment would fail until it's completed
            payment.charge_with_stripe()
            payment.set_status("complete")  # charge succeeded
            return payment.json(), 200
        # the following error handling is advised by Stripe, although the handling implementations are identical,
        # we choose to specify them separately just to give the students a better idea what we can expect
        except error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            return e.json_body, e.http_status
        except error.RateLimitError as e:
            # Too many requests made to the API too quickly
            return e.json_body, e.http_status
        except error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            return e.json_body, e.http_status
        except error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return e.json_body, e.http_status
        except error.APIConnectionError as e:
            # Network communication with Stripe failed
            return e.json_body, e.http_status
        except error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return e.json_body, e.http_status
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {"message": "payment_error"}, 500

class AllPayments(Resource):
    def get(self):
        allPayments=PaymentModel.query.all()
        return [payment.json() for payment in allPayments ]
