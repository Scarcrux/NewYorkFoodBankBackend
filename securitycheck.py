from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User

def authenticate(username,password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()
