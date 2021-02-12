from time import time
from uuid import uuid4
from app import db

CONFIRMATION_EXPIRATION_DELTA = 1800  # 30 minutes

class ConfirmationModel(db.Model):
    __tablename__ = "confirmations"

    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User")

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.confirmed = False

    def expired(self):
        return time() > self.expire_at

    def force_to_expire(self):  # forcing current confirmation to expire
        if not self.expired:
            self.expire_at = int(time())
            db.session.add(self)
            db.session.commit()
    
    def json(self):
        return {
            'expire_at': self.expire_at,
            'confirmed': self.confirmed,
            'user_id': self.user_id
        }