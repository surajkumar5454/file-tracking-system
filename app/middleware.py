from functools import wraps
from flask import request, abort
import magic
import hashlib
from datetime import datetime

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or not validate_api_key(api_key):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

def validate_file_type(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'file' not in request.files:
            abort(400)
            
        file = request.files['file']
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file.read())
        file.seek(0)  # Reset file pointer
        
        ALLOWED_MIMES = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/jpeg',
            'image/png'
        ]
        
        if file_type not in ALLOWED_MIMES:
            abort(400, 'Invalid file type')
            
        return f(*args, **kwargs)
    return decorated_function 