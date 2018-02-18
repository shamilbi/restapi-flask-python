from werkzeug.security import safe_str_cmp
from models.user import User


def authenticate(username, password):
    user = User.by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user
    return None


def identity(payload):
    user_id = payload['identity']
    return User.by_id(user_id)
