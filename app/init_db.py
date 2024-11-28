from app import create_app, db
from app.models.user import User, Role
from werkzeug.security import generate_password_hash

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create roles if they don't exist
        roles = [
            'DG', 'ADG', 'DIG', 'SE', 'EE', 'IFA', 
            'Budget_Officer', 'Estate_Officer', 'Branch_Diary'
        ]
        
        for role_name in roles:
            if not Role.query.filter_by(name=role_name).first():
                role = Role(name=role_name)
                db.session.add(role)
        
        # Create admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin_role = Role.query.filter_by(name='DG').first()
            admin = User(
                username='admin',
                email='admin@example.com',
                department='Administration',
                role=admin_role
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()