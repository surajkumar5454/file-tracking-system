from app.extensions import db
from datetime import datetime

class Proposal(db.Model):
    __tablename__ = 'proposals'
    
    # Status constants
    STATUS_PENDING = 'pending_approval'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    
    id = db.Column(db.Integer, primary_key=True)
    file_number = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    department = db.Column(db.String(100))
    estimated_cost = db.Column(db.Float)
    priority = db.Column(db.String(20))
    current_status = db.Column(db.String(50), default=STATUS_PENDING)
    current_location = db.Column(db.String(50))  # Role name of current handler
    originator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    movements = db.relationship('FileMovement', backref='proposal', lazy=True)
    documents = db.relationship('Document', backref='proposal', lazy=True)
    originator = db.relationship('User', foreign_keys=[originator_id], backref='proposals')

class FileMovement(db.Model):
    __tablename__ = 'file_movements'
    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'))
    from_department = db.Column(db.String(100))
    to_department = db.Column(db.String(100))
    action = db.Column(db.String(100))
    comments = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    moved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationship with User who moved the file
    user = db.relationship('User', foreign_keys=[moved_by], backref='file_movements')

class ProposalHistory(db.Model):
    __tablename__ = 'proposal_history'
    
    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(50), nullable=False)  # e.g., 'created', 'forwarded', 'approved', 'rejected'
    from_role = db.Column(db.String(50))
    to_role = db.Column(db.String(50))
    comments = db.Column(db.Text)
    
    # Relationship with Proposal
    proposal = db.relationship('Proposal', backref=db.backref('history', lazy=True))

    def __repr__(self):
        return f'<ProposalHistory {self.action} at {self.timestamp}>'