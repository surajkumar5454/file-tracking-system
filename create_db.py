from app import create_app, db
from app.models.user import User, Role
from app.models.proposal import Proposal
from app.models.file_movement import FileMovement

def create_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created.")

        # Initialize roles and users
        roles = [
            'DG', 'ADG', 'DIG_Works', 'SE', 'EE', 'IFA', 
            'DC_Finance', 'Budget', 'AC_Estate', 'Branch_Diary'
        ]
        
        for role_name in roles:
            if not Role.query.filter_by(name=role_name).first():
                role = Role(name=role_name)
                db.session.add(role)
        
        db.session.commit()
        print("Roles created.")

        # Create default users
        for role in Role.query.all():
            username = role.name.lower()
            if not User.query.filter_by(username=username).first():
                user = User(
                    username=username,
                    email=f"{username}@example.com",
                    role=role
                )
                user.set_password('password123')
                db.session.add(user)
        
        db.session.commit()
        print("Users created.")

if __name__ == '__main__':
    create_database() 