from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models.proposal import Proposal, FileMovement, ProposalHistory
from datetime import datetime

proposal_bp = Blueprint('proposal', __name__, url_prefix='/proposals')

@proposal_bp.route('/<int:id>/approve', methods=['POST'])
@login_required
def approve(id):
    proposal = Proposal.query.get_or_404(id)
    
    if proposal.current_location != current_user.role.name:
        flash('You do not have permission to approve this proposal', 'error')
        return redirect(url_for('main.dashboard'))
    
    comments = request.form.get('comments')
    
    # Update proposal status
    proposal.current_status = Proposal.STATUS_APPROVED
    proposal.updated_at = datetime.utcnow()
    
    # Create history record
    history = ProposalHistory(
        proposal_id=proposal.id,
        action='approved',
        from_role=current_user.role.name,
        to_role=current_user.role.name,
        comments=comments
    )
    
    db.session.add(history)
    db.session.commit()
    
    flash('Proposal approved successfully', 'success')
    return redirect(url_for('main.dashboard'))

@proposal_bp.route('/<int:id>/reject', methods=['POST'])
@login_required
def reject(id):
    proposal = Proposal.query.get_or_404(id)
    
    if proposal.current_location != current_user.role.name:
        flash('You do not have permission to reject this proposal', 'error')
        return redirect(url_for('main.dashboard'))
    
    comments = request.form.get('comments')
    
    # Update proposal status
    proposal.current_status = Proposal.STATUS_REJECTED
    proposal.updated_at = datetime.utcnow()
    
    # Create history record
    history = ProposalHistory(
        proposal_id=proposal.id,
        action='rejected',
        from_role=current_user.role.name,
        to_role=current_user.role.name,
        comments=comments
    )
    
    db.session.add(history)
    db.session.commit()
    
    flash('Proposal rejected successfully', 'success')
    return redirect(url_for('main.dashboard'))

@proposal_bp.route('/<int:id>/forward', methods=['POST'])
@login_required
def forward(id):
    proposal = Proposal.query.get_or_404(id)
    
    if proposal.current_location != current_user.role.name:
        flash('You do not have permission to forward this proposal', 'error')
        return redirect(url_for('main.dashboard'))
    
    forward_to = request.form.get('forward_to')
    comments = request.form.get('comments')
    
    if not forward_to:
        flash('Please select a role to forward to', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Update proposal location
    proposal.current_location = forward_to
    proposal.current_status = Proposal.STATUS_PENDING
    proposal.updated_at = datetime.utcnow()
    
    # Create history record
    history = ProposalHistory(
        proposal_id=proposal.id,
        action='forwarded',
        from_role=current_user.role.name,
        to_role=forward_to,
        comments=comments
    )
    
    db.session.add(history)
    db.session.commit()
    
    flash('Proposal forwarded successfully', 'success')
    return redirect(url_for('main.dashboard')) 