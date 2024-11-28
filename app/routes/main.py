from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.proposal import Proposal, FileMovement, ProposalHistory
from app.models.user import User, Role
from app.extensions import db
from datetime import datetime
from app.forms import ProposalForm
from app.utils.hierarchy import get_subordinate_roles

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get subordinate roles
    subordinate_roles = get_subordinate_roles(current_user.role.name)
    print(f"Current Role: {current_user.role.name}")
    print(f"Subordinate Roles: {subordinate_roles}")
    
    # Get direct proposals (where user is originator or current handler)
    direct_proposals = Proposal.query.filter(
        db.or_(
            Proposal.originator_id == current_user.id,
            Proposal.current_location == current_user.role.name
        )
    ).order_by(Proposal.updated_at.desc()).all()
    print(f"Direct Proposals: {len(direct_proposals)}")

    # Get subordinate proposals (pending with subordinate roles)
    subordinate_proposals = []
    subordinate_counts = {}

    if subordinate_roles:
        # Query all proposals at subordinate levels
        subordinate_query = Proposal.query.filter(
            Proposal.current_location.in_(subordinate_roles)
        )
        print(f"Subordinate Query: {str(subordinate_query)}")
        
        subordinate_proposals = subordinate_query.order_by(
            Proposal.current_location,
            Proposal.updated_at.desc()
        ).all()
        print(f"Subordinate Proposals: {len(subordinate_proposals)}")

        # Group proposals by role for statistics
        for role in subordinate_roles:
            role_proposals = [p for p in subordinate_proposals if p.current_location == role]
            if role_proposals:
                subordinate_counts[role] = {
                    'total': len(role_proposals),
                    'pending': sum(1 for p in role_proposals if p.current_status == 'pending_approval'),
                    'approved': sum(1 for p in role_proposals if p.current_status == 'approved'),
                    'rejected': sum(1 for p in role_proposals if p.current_status == 'rejected')
                }
                print(f"Role {role} stats: {subordinate_counts[role]}")

    # Direct proposal counts
    direct_total = len(direct_proposals)
    direct_pending = sum(1 for p in direct_proposals 
                        if p.current_status == 'pending_approval' 
                        and p.current_location == current_user.role.name)
    direct_approved = sum(1 for p in direct_proposals 
                         if p.current_status == 'approved')
    direct_rejected = sum(1 for p in direct_proposals 
                         if p.current_status == 'rejected')

    # Calculate total subordinate statistics
    subordinate_total = len(subordinate_proposals)
    subordinate_pending = sum(1 for p in subordinate_proposals 
                            if p.current_status == 'pending_approval')
    subordinate_approved = sum(1 for p in subordinate_proposals 
                             if p.current_status == 'approved')
    subordinate_rejected = sum(1 for p in subordinate_proposals 
                             if p.current_status == 'rejected')

    # Get available roles for forwarding
    available_roles = [
        {'name': 'DG', 'title': 'Director General'},
        {'name': 'ADG', 'title': 'Additional Director General'},
        {'name': 'DIG', 'title': 'DIG (Works)'},
        {'name': 'SE', 'title': 'Superintending Engineer'},
        {'name': 'EE', 'title': 'Executive Engineer'},
        {'name': 'IFA', 'title': 'Internal Financial Advisor'},
        {'name': 'Budget_Officer', 'title': 'Budget Officer'},
        {'name': 'Estate_Officer', 'title': 'Estate Officer'},
        {'name': 'Branch_Diary', 'title': 'Branch Diary'}
    ]
    
    # Get role titles for display
    role_titles = {role['name']: role['title'] for role in available_roles}
    
    return render_template('dashboard.html',
                         direct_proposals=direct_proposals,
                         subordinate_proposals=subordinate_proposals,
                         direct_total=direct_total,
                         direct_pending=direct_pending,
                         direct_approved=direct_approved,
                         direct_rejected=direct_rejected,
                         subordinate_total=subordinate_total,
                         subordinate_pending=subordinate_pending,
                         subordinate_approved=subordinate_approved,
                         subordinate_rejected=subordinate_rejected,
                         subordinate_counts=subordinate_counts,
                         subordinate_roles=subordinate_roles,
                         available_roles=available_roles,
                         role_titles=role_titles)

@main_bp.route('/track_file')
@login_required
def track_file():
    file_number = request.args.get('file_number')
    
    if file_number:
        # Directly fetch the proposal and its history
        proposal = Proposal.query.filter_by(file_number=file_number).first()
        
        if proposal:
            history = ProposalHistory.query.filter_by(
                proposal_id=proposal.id
            ).order_by(ProposalHistory.timestamp.desc()).all()
            
            return render_template('proposal/track_result.html', 
                                 proposal=proposal, 
                                 history=history)
        else:
            flash('Proposal not found.', 'danger')
            return redirect(url_for('main.dashboard'))
    
    # If no file number provided, show the search form
    return render_template('proposal/track.html')

@main_bp.route('/submit_proposal', methods=['GET', 'POST'])
@login_required
def submit_proposal():
    if request.method == 'GET':
        # Define the available roles for forwarding
        available_roles = [
            {'name': 'DG', 'title': 'Director General'},
            {'name': 'ADG', 'title': 'Additional Director General'},
            {'name': 'DIG', 'title': 'DIG (Works)'},
            {'name': 'SE', 'title': 'Superintending Engineer'},
            {'name': 'EE', 'title': 'Executive Engineer'},
            {'name': 'IFA', 'title': 'Internal Financial Advisor'},
            {'name': 'BUDGET_OFFICER', 'title': 'Budget Officer'},
            {'name': 'ESTATE_OFFICER', 'title': 'Estate Officer'},
            {'name': 'BRANCH_DIARY', 'title': 'Branch Diary'}
        ]
        # Remove current user's role from the list
        available_roles = [role for role in available_roles if role['name'] != current_user.role.name]
        return render_template('proposal/new.html', available_roles=available_roles)
    
    try:
        # Get form data
        forward_to = request.form.get('forward_to').upper()  # Ensure uppercase
        file_number = request.form.get('file_number')
        title = request.form.get('title')
        description = request.form.get('description')
        department = request.form.get('department')
        estimated_cost = float(request.form.get('estimated_cost', 0))
        priority = request.form.get('priority', 'normal')
        comments = request.form.get('comments')
        
        # Create new proposal
        proposal = Proposal(
            file_number=file_number,
            title=title,
            description=description,
            department=department,
            estimated_cost=estimated_cost,
            priority=priority,
            current_status='pending_approval',
            current_location=forward_to,  # Set to forwarded role
            originator_id=current_user.id
        )
        
        db.session.add(proposal)
        db.session.commit()
        
        # Create initial history record
        history = ProposalHistory(
            proposal_id=proposal.id,
            action='created',
            from_role=current_user.role.name,
            to_role=forward_to,
            comments=comments or 'Proposal created and forwarded'
        )
        
        db.session.add(history)
        db.session.commit()
        
        flash('Proposal submitted and forwarded successfully', 'success')
        return redirect(url_for('main.dashboard'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating proposal: {str(e)}', 'error')
        return redirect(url_for('main.dashboard')) 

@main_bp.route('/debug_roles')
@login_required
def debug_roles():
    all_proposals = Proposal.query.all()
    all_users = User.query.all()
    
    debug_info = {
        'current_user': {
            'username': current_user.username,
            'role': current_user.role.name,
            'subordinates': get_subordinate_roles(current_user.role.name)
        },
        'proposals': [{
            'id': p.id,
            'title': p.title,
            'current_location': p.current_location,
            'status': p.current_status
        } for p in all_proposals],
        'users': [{
            'username': u.username,
            'role': u.role.name
        } for u in all_users]
    }
    
    return render_template('debug_roles.html', debug_info=debug_info) 