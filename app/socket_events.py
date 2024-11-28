from flask_socketio import SocketIO, emit
from flask_login import current_user
from app import db

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        return False
    
    # Join user's personal room
    room = f'user_{current_user.id}'
    join_room(room)
    
    # Send initial notification count
    unread_count = Notification.query.filter_by(
        user_id=current_user.id,
        read=False
    ).count()
    
    emit('notification_count', {'count': unread_count})

def notify_user(user_id, notification_data):
    """Utility function to send real-time notifications"""
    room = f'user_{user_id}'
    emit('new_notification', notification_data, room=room) 