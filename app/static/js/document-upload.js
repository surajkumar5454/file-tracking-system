class DocumentManager {
    constructor() {
        this.dropzone = null;
        this.historyContainer = document.getElementById('document-history');
        this.detailsContainer = document.getElementById('selected-document-details');
        this.initializeDropzone();
        this.loadDocumentHistory();
    }
    
    initializeDropzone() {
        Dropzone.autoDiscover = false;
        
        this.dropzone = new Dropzone("#document-upload-form", {
            url: "/api/documents/upload",
            maxFilesize: 10, // MB
            acceptedFiles: ".pdf,.doc,.docx,.jpg,.jpeg,.png",
            addRemoveLinks: true,
            headers: {
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
            },
            init: function() {
                this.on("success", (file, response) => {
                    this.loadDocumentHistory();
                    showNotification('Document uploaded successfully', 'success');
                });
                
                this.on("error", (file, errorMessage) => {
                    showNotification(errorMessage, 'error');
                });
            }
        });
    }
    
    async loadDocumentHistory() {
        try {
            const response = await fetch('/api/documents/history');
            const documents = await response.json();
            
            this.historyContainer.innerHTML = documents.map(doc => `
                <div class="document-item" data-id="${doc.id}">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <i class="fas ${this.getFileIcon(doc.file_type)}"></i>
                            <span>${doc.filename}</span>
                        </div>
                        <div>
                            <small class="text-muted">${doc.uploaded_at}</small>
                            <div class="btn-group">
                                <button class="btn btn-sm btn-primary view-btn">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="btn btn-sm btn-danger delete-btn">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
            
            this.addEventListeners();
            
        } catch (error) {
            showNotification('Error loading document history', 'error');
        }
    }
    
    getFileIcon(fileType) {
        const icons = {
            'application/pdf': 'fa-file-pdf',
            'application/msword': 'fa-file-word',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'fa-file-word',
            'image/jpeg': 'fa-file-image',
            'image/png': 'fa-file-image'
        };
        return icons[fileType] || 'fa-file';
    }
    
    addEventListeners() {
        this.historyContainer.querySelectorAll('.document-item').forEach(item => {
            const id = item.dataset.id;
            
            item.querySelector('.view-btn').addEventListener('click', () => {
                this.viewDocument(id);
            });
            
            item.querySelector('.delete-btn').addEventListener('click', () => {
                this.deleteDocument(id);
            });
            
            item.addEventListener('click', () => {
                this.showDocumentDetails(id);
            });
        });
    }
    
    async viewDocument(id) {
        window.open(`/api/documents/${id}/view`, '_blank');
    }
    
    async deleteDocument(id) {
        if (!confirm('Are you sure you want to delete this document?')) return;
        
        try {
            const response = await fetch(`/api/documents/${id}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
                }
            });
            
            if (response.ok) {
                this.loadDocumentHistory();
                showNotification('Document deleted successfully', 'success');
            } else {
                throw new Error('Failed to delete document');
            }
        } catch (error) {
            showNotification('Error deleting document', 'error');
        }
    }
    
    async showDocumentDetails(id) {
        try {
            const response = await fetch(`/api/documents/${id}/details`);
            const details = await response.json();
            
            this.detailsContainer.innerHTML = `
                <div class="document-details">
                    <h5>${details.filename}</h5>
                    <p><strong>Size:</strong> ${details.file_size_formatted}</p>
                    <p><strong>Type:</strong> ${details.file_type}</p>
                    <p><strong>Uploaded by:</strong> ${details.uploaded_by}</p>
                    <p><strong>Version:</strong> ${details.version}</p>
                    <p><strong>Upload date:</strong> ${details.uploaded_at}</p>
                    
                    <div class="mt-3">
                        <h6>Version History</h6>
                        <ul class="list-unstyled">
                            ${details.versions.map(v => `
                                <li>
                                    <small>v${v.version} - ${v.uploaded_at}</small>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            `;
        } catch (error) {
            showNotification('Error loading document details', 'error');
        }
    }
}

// Initialize document manager
const documentManager = new DocumentManager();