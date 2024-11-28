from app import create_app
from app.extensions import db
from app.models.user import User, Role

def init_test_data():
    app = create_app()
    with app.app_context():
        # First delete all existing data to start fresh
        try:
            User.query.delete()
            Role.query.delete()
            db.session.commit()
        except:
            db.session.rollback()

        # Create test roles
        roles_data = [
            {'name': 'DG', 'description': 'Director General'},
            {'name': 'ADG', 'description': 'Additional Director General'},
            {'name': 'DIG', 'description': 'DIG (Works)'},
            {'name': 'SE', 'description': 'Superintending Engineer'},
            {'name': 'EE', 'description': 'Executive Engineer'},
            {'name': 'IFA', 'description': 'Internal Financial Advisor'},
            {'name': 'Budget_Officer', 'description': 'Budget Officer'},
            {'name': 'Estate_Officer', 'description': 'Estate Officer'},
            {'name': 'Branch_Diary', 'description': 'Branch Diary'}
        ]
        
        try:
            # Create roles and users
            for role_data in roles_data:
                # Create role
                role = Role(name=role_data['name'], description=role_data['description'])
                db.session.add(role)
                db.session.flush()  # To get the role.id
                
                # Create test user for this role
                username = role_data['name'].lower()
                user = User(
                    username=username,
                    email=f"{username}@example.com",
                    department='Administration',
                    role=role,
                    is_active=True
                )
                user.set_password('test123')  # Set same password for all test users
                db.session.add(user)
            
            db.session.commit()
            print("Test data initialized successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing test data: {str(e)}")

if __name__ == '__main__':
    init_test_data()