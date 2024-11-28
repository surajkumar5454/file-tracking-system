from app.models.user import User, Role
from app.models.proposal import Proposal, FileMovement
from app.models.document import Document
from app.models.workflow import ProposalWorkflow, WorkflowHistory

# This ensures all models are imported when 'app.models' is imported
__all__ = [
    'User', 'Role', 
    'Proposal', 'FileMovement',
    'Document',
    'ProposalWorkflow', 'WorkflowHistory'
] 