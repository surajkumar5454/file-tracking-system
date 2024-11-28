from app.extensions import db
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_type = db.Column(db.String(100))
    file_size = db.Column(db.Integer)  # in bytes
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Version tracking
    version = db.Column(db.Integer, default=1)
    is_current = db.Column(db.Boolean, default=True)
    
    # Relationship with User who uploaded the document
    uploader = db.relationship('User', foreign_keys=[uploaded_by], backref='uploaded_documents')
    
    @property
    def file_size_formatted(self):
        """Return human-readable file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024