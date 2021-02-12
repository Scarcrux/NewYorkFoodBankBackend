from requests import Response
from flask import request, url_for

from models.confirmation import ConfirmationModel
from libs.mailgun import Mailgun
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class User(db.Model):

    # Create a table in the db
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)

    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def most_recent_confirmation(self):
        # ordered by expiration time (in descending order)
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    def send_confirmation_email(self):
        subject = "Registration Confirmation"
        link = request.url_root[:-1] + url_for(
            "confirmation", confirmation_id=self.most_recent_confirmation().id
        )
        text = f"Please click the link to confirm your registration: {link}"
        return Mailgun.send_email([self.email], subject, text)

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    def json(self):
        return {
            'email': self.email,
            'username': self.username
        }

