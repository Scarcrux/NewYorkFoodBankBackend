from requests import Response
from flask import request, url_for
from db import db

from models.confirmation import Confirmation
from libs.mailgun import Mailgun
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(80), nullable=False, unique=True)
    confirmation = db.relationship(
        "Confirmation", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __init__(self, username, password, email):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email

    def json(self):
        return {'name':self.username,'password':self.password_hash, 'email':self.email}

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def most_recent_confirmation(self):
        # ordered by expiration time (in descending order)
        return self.confirmation.order_by(db.desc(Confirmation.expire_at)).first()

    def send_confirmation_email(self) -> Response:
        subject = "Registration Confirmation"
        link = request.url_root[:-1] + url_for(
            "confirmation", confirmation_id=self.most_recent_confirmation.id
        )
        text = f"Please click the link to confirm your registration: {link}"
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        return Mailgun.send_email([self.email], subject, text, html)

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

