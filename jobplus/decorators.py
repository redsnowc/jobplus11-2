from flask import abort
from flask_login import current_user
from functools import wraps
from jobplus.models import User

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwrargs):
            if role == 30:
                if not current_user.is_authenticated or (
                        current_user.role < role):
                    abort(404)
                return func(*args, **kwrargs)
            else:
                if not current_user.is_authenticated or (
                        current_user.role != role):
                    abort(404)
                return func(*args, **kwrargs)
        return wrapper
    return decorator

user_required = role_required(User.ROLE_USER)
company_required = role_required(User.ROLE_COMPANY)
admin_required = role_required(User.ROLE_ADMIN)
