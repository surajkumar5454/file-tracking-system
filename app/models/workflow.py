from app.extensions import db
from datetime import datetime

class WorkflowStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50))
    step_order = db.Column(db.Integer)
    can_approve = db.Column(db.Boolean, default=False)
    can_reject = db.Column(db.Boolean, default=False)
    next_steps = db.Column(db.JSON)  # Possible next departments

class ProposalWorkflow(db.Model):
    __tablename__ = 'proposal_workflow'
    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposals.id'))
    current_step = db.Column(db.Integer, default=1)
    current_department = db.Column(db.String(100))
    status = db.Column(db.String(50))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    proposal = db.relationship('Proposal', backref='workflow')
    updater = db.relationship('User', foreign_keys=[updated_by], backref='workflow_updates')

class WorkflowHistory(db.Model):
    __tablename__ = 'workflow_history'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('proposal_workflow.id'))
    from_department = db.Column(db.String(100))
    to_department = db.Column(db.String(100))
    action = db.Column(db.String(50))
    comments = db.Column(db.Text)
    acted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    workflow = db.relationship('ProposalWorkflow', backref='history')
    actor = db.relationship('User', foreign_keys=[acted_by], backref='workflow_actions') 