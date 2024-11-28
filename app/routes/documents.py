from app.security.virus_scan import SecurityManager
from app.models.audit import AuditLog

security_manager = SecurityManager()

@bp.route('/upload', methods=['POST'])
@login_required
@validate_file_type
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp', secure_filename(file.filename))
    file.save(temp_path)
    
    # Virus scan
    if not security_manager.scan_file(temp_path):
        os.remove(temp_path)
        return jsonify({'error': 'File failed security scan'}), 400
    
    # Calculate hash
    file_hash = security_manager.calculate_file_hash(temp_path)
    
    # Encrypt file
    encrypted_path = security_manager.encrypt_file(temp_path)
    if not encrypted_path:
        os.remove(temp_path)
        return jsonify({'error': 'File encryption failed'}), 500
    
    try:
        document = Document(
            filename=secure_filename(file.filename),
            original_filename=file.filename,
            file_path=encrypted_path,
            file_type=file.content_type,
            file_size=os.path.getsize(temp_path),
            file_hash=file_hash,
            uploaded_by=current_user.id
        )
        
        db.session.add(document)
        db.session.commit()
        
        # Log audit
        AuditLog.log_action(
            user_id=current_user.id,
            action='upload',
            entity_type='document',
            entity_id=document.id,
            details={'filename': document.filename, 'hash': file_hash},
            request=request
        )
        
        return jsonify({
            'id': document.id,
            'filename': document.filename,
            'size': document.file_size_formatted
        })
        
    finally:
        os.remove(temp_path) 