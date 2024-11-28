from flask import Flask
from config import Config
from app.extensions import db, login_manager, migrate
from flask_migrate import Migrate

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'

    with app.app_context():
        # Import blueprints inside app context
        from app.routes.main import main_bp
        from app.routes.auth import auth_bp
        from app.routes.admin import admin_bp
        from app.routes.proposal import proposal_bp
        
        # Register blueprints
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(proposal_bp)

    return app 