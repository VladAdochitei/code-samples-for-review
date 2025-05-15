from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)  # Forbidden
            if role == 'admin' and not current_user.role == 'admin':
                abort(403)  # Forbidden
            return func(*args, **kwargs)
        return wrapper
    return decorator

def forbid_admin_route(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':
            abort(403)  # Forbidden for admin
        return func(*args, **kwargs)
    return wrapper