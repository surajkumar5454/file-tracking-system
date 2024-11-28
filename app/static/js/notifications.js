class NotificationManager {
    constructor() {
        this.container = document.getElementById('notifications-container');
        this.badge = document.getElementById('notifications-badge');
        this.initialized = false;
    }
    
    init() {
        if (this.initialized) return;
        this.loadNotifications();
        setInterval(() => this.loadNotifications(), 30000); // Check every 30 seconds
        this.initialized = true;
    }
    
    async loadNotifications() {
        const response = await fetch('/api/notifications');
        const notifications = await response.json();
        
        this.badge.textContent = notifications.length;
        this.updateNotificationsList(notifications);
    }
    
    updateNotificationsList(notifications) {
        this.container.innerHTML = notifications.map(n => `
            <div class="notification-item ${n.type}" data-id="${n.id}">
                <h6>${n.title}</h6>
                <p>${n.message}</p>
                <small>${n.created_at}</small>
            </div>
        `).join('');
        
        // Add click handlers
        this.container.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', () => this.markAsRead(item.dataset.id));
        });
    }
    
    async markAsRead(notificationId) {
        await fetch('/api/notifications/mark-read', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                notification_ids: [notificationId]
            })
        });
        
        this.loadNotifications();
    }
}

// Initialize notification manager
const notificationManager = new NotificationManager();
document.addEventListener('DOMContentLoaded', () => notificationManager.init()); 