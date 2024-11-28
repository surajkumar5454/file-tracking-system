from flask import Blueprint, render_template, jsonify, request, send_file
from flask_login import login_required
from app.models.proposal import Proposal, WorkflowHistory
from app.models.user import User
from sqlalchemy import func
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.route('/dashboard')
@login_required
def analytics_dashboard():
    # Get basic statistics
    total_proposals = Proposal.query.count()
    pending_proposals = Proposal.query.filter_by(current_status='submitted').count()
    completed_proposals = Proposal.query.filter_by(current_status='approved').count()
    
    # Get department-wise statistics
    dept_stats = db.session.query(
        User.department,
        func.count(Proposal.id).label('proposal_count')
    ).join(Proposal, User.id == Proposal.originator_id)\
     .group_by(User.department).all()
    
    # Get timeline data
    timeline_data = db.session.query(
        func.date(Proposal.created_at),
        func.count(Proposal.id)
    ).group_by(func.date(Proposal.created_at))\
     .order_by(func.date(Proposal.created_at)).all()
    
    return render_template('reports/dashboard.html',
                         total_proposals=total_proposals,
                         pending_proposals=pending_proposals,
                         completed_proposals=completed_proposals,
                         dept_stats=dept_stats,
                         timeline_data=timeline_data)

@bp.route('/export')
@login_required
def export_report():
    start_date = request.args.get('start_date', default=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', default=datetime.now().strftime('%Y-%m-%d'))
    
    proposals = Proposal.query.filter(
        Proposal.created_at.between(start_date, end_date)
    ).all()
    
    # Create DataFrame
    data = []
    for proposal in proposals:
        data.append({
            'Proposal ID': proposal.proposal_id,
            'Title': proposal.title,
            'Status': proposal.current_status,
            'Created Date': proposal.created_at,
            'Originator': proposal.originator.username,
            'Department': proposal.originator.department
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Proposals', index=False)
    
    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'proposal_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
    ) 