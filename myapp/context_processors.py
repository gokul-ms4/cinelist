from .models import *


def notifications(request):
    if request.user.is_authenticated:
        if request.path == '/user/notification/':
            NotificationModel.objects.filter(
                receiver=request.user,
                is_read=False
            ).update(is_read=True)

        notifs = NotificationModel.objects.filter(
            receiver=request.user
        ).select_related('sender').order_by('-created_at')

        unread = notifs.filter(is_read=False).count()

        return {
            'notifications': notifs,
            'notification_count': notifs.count(),
            'unread_count': unread,
        }
    
    return {
        'notifications': [],
        'notification_count': 0,
        'unread_count': 0,
    }