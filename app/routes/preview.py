from flask import Blueprint, send_file, abort
from flask_login import login_required
from PIL import Image
import io
import os

bp = Blueprint('preview', __name__, url_prefix='/preview')

@bp.route('/document/<int:document_id>')
@login_required
def preview_document(document_id):
    document = Document.query.get_or_404(document_id)
    
    # Check permissions
    if not current_user.can_view_document(document):
        abort(403)
    
    file_ext = os.path.splitext(document.filename)[1].lower()
    
    try:
        if file_ext in ['.jpg', '.jpeg', '.png']:
            return preview_image(document)
        else:
            # For non-image files, return a generic preview or download
            return send_file(
                document.file_path,
                as_attachment=True,
                download_name=document.filename
            )
    except Exception as e:
        abort(500)

def preview_image(document):
    with Image.open(document.file_path) as img:
        # Create thumbnail
        img.thumbnail((800, 800))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        img_byte_arr.seek(0)
        
        return send_file(
            img_byte_arr,
            mimetype=f'image/{img.format.lower()}'
        ) 