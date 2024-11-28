from flask import Blueprint

# Import routes
from .auth import auth_bp
from .main import main_bp
from .admin import admin_bp
from .proposal import proposal_bp

# Register blueprints in __init__.py 