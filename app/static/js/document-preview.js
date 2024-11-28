class DocumentPreview {
    constructor() {
        this.modal = null;
        this.createModal();
    }
    
    createModal() {
        this.modal = document.createElement('div');
        this.modal.className = 'preview-modal';
        this.modal.style.display = 'none';
        document.body.appendChild(this.modal);
        
        // Close on click outside
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.hidePreview();
            }
        });
    }
    
    async showPreview(documentId) {
        try {
            const response = await fetch(`/preview/document/${documentId}`);
            if (!response.ok) throw new Error('Preview failed');
            
            const blob = await response.blob();
            const objectUrl = URL.createObjectURL(blob);
            
            this.modal.innerHTML = `
                <div class="preview-content">
                    <div class="preview-header">
                        <button class="close-btn">&times;</button>
                    </div>
                    <div class="preview-body">
                        <img src="${objectUrl}" style="max-width: 100%; height: auto;">
                    </div>
                </div>
            `;
            
            this.modal.style.display = 'flex';
            
            // Add close button handler
            this.modal.querySelector('.close-btn').addEventListener('click', () => {
                this.hidePreview();
            });
            
        } catch (error) {
            showNotification('Error loading preview', 'error');
        }
    }
    
    hidePreview() {
        this.modal.style.display = 'none';
        this.modal.innerHTML = '';
    }
}

// Initialize preview handler
const documentPreview = new DocumentPreview(); 