from app import db
from datetime import datetime

class FileMovement(db.Model):
    __tablename__ = 'file_movement'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal.id'), nullable=False)
    from_department = db.Column(db.String(100))
    to_department = db.Column(db.String(100))
    action = db.Column(db.String(100))
    comments = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User who moved the file
    moved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='file_movements')
    
    # Relationship with proposal
    proposal = db.relationship('Proposal', backref='movements')

    def __repr__(self):
        return f'<FileMovement {self.id}>'
    