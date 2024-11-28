from app import create_app, db
from app.models.proposal import Proposal, FileMovement, ProposalHistory
from app.models.user import User, Role
from sqlalchemy import inspect

def upgrade():
    """Create new tables and add new columns"""
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Create ProposalHistory table
        if 'proposal_history' not in inspector.get_table_names():
            class ProposalHistory(db.Model):
                __tablename__ = 'proposal_history'
                id = db.Column(db.Integer, primary_key=True)
                proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'), nullable=False)
                timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
                action = db.Column(db.String(50), nullable=False)
                from_role = db.Column(db.String(50))
                to_role = db.Column(db.String(50))
                comments = db.Column(db.Text)

            db.create_all()
            print("Created proposal_history table")

            # Migrate existing FileMovement records to ProposalHistory
            try:
                movements = FileMovement.query.all()
                for movement in movements:
                    history = ProposalHistory(
                        proposal_id=movement.proposal_id,
                        timestamp=movement.timestamp,
                        action=movement.action,
                        from_role=movement.from_department,
                        to_role=movement.to_department,
                        comments=movement.comments
                    )
                    db.session.add(history)
                
                db.session.commit()
                print("Migrated existing file movements to proposal history")
            except Exception as e:
                db.session.rollback()
                print(f"Error migrating data: {str(e)}")
        else:
            print("ProposalHistory table already exists")

def downgrade():
    """Remove tables and columns"""
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Drop ProposalHistory table if it exists
        if 'proposal_history' in inspector.get_table_names():
            ProposalHistory.__table__.drop(db.engine)
            print("Dropped proposal_history table")
        else:
            print("ProposalHistory table does not exist")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'downgrade':
            downgrade()
        else:
            print("Unknown command. Use 'downgrade' to remove tables.")
    else:
        upgrade() 