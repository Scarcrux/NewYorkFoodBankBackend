import os
import stripe

from app import db
from typing import List

CURRENCY = "usd"

class PaymentModel(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, amount, status, user_id):
         self.amount=amount
         self.status=status
         self.user_id=user_id

    def description(self):
        """
        Generates a simple string representing this order, in the format of "5x chair, 2x table"
        """
        return "Donated ".join(self.amount)

    def charge_with_stripe(self):

        stripe.api_key = os.environ.get("STRIPE_API_KEY")

        token = stripe.Token.create(
            card={
                "number": "4242424242424242",
                "exp_month": 2,
                "exp_year": 2022,
                "cvc": "314",
                },
                )

        return stripe.Charge.create(
            amount=self.amount,  # amount of cents (100 means USD$1.00)
            currency=CURRENCY,
            source=token["id"],
            description="self.description()"
        )

    def set_status(self, new_status):
        self.status = new_status
        db.session.commit()

    def json(self):
        return {
            'amount': self.amount,
            'status': self.status,
            'user_id': self.user_id
        }