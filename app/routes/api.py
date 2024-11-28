from flask import request, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.models.document import Document
import os

@bp.route('/documents/history')
@login_required
def get_document_history():
    documents = Document.query.filter_by(
        proposal_id=request.args.get('proposal_id')
    ).order_by(Document.uploaded_at.desc()).all()
    
    return jsonify([{
        'id': doc.id,
        'filename': doc.original_filename,
        'file_type': doc.file_type,
        'file_size': doc.file_size_formatted,
        'uploaded_at': doc.uploaded_at.strftime('%Y-%m-%d %H:%M'),
        'version': doc.version
    } for doc in documents])

@bp.route('/documents/<int:document_id>/details')
@login_required
def get_document_details(document_id):
    document = Document.query.get_or_404(document_id)
    
    # Get version history
    versions = Document.query.filter_by(
        original_filename=document.original_filename,
        proposal_id=document.proposal_id
    ).order_by(Document.version.desc()).all()
    
    return jsonify({
        'id': document.id,
        'filename': document.original_filename,
        'file_type': document.file_type,
        'file_size_formatted': document.file_size_formatted,
        'uploaded_by': document.uploaded_by.username,
        'uploaded_at': document.uploaded_at.strftime('%Y-%m-%d %H:%M'),
        'version': document.version,
        'versions': [{
            'version': v.version,
            'uploaded_at': v.uploaded_at.strftime('%Y-%m-%d %H:%M')
        } for v in versions]
    })

@bp.route('/documents/<int:document_id>', methods=['DELETE'])
@login_required
@require_api_key
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    
    # Check permissions
    if not current_user.can_delete_document(document):
        abort(403)
    
    # Delete file from storage
    try:
        os.remove(document.file_path)
    except OSError:
        pass
    
    db.session.delete(document)
    db.session.commit()
    
    return jsonify({'status': 'success'}) 