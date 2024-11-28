from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role.name not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def department_required(departments):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.department not in departments:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def permission_required(roles):
    """Alias for role_required for backward compatibility"""
    return role_required(roles) 