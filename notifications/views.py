from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from notifications.models import Notification

# Create your views here.
User = get_user_model()

def send_notification(request, user_id):
    user = get_object_or_404(User, id=user_id)
    Notification.objects.create(
        user = user,
        title = "New notification",
        message = "You have a new notification",
        notification_type = "info"
    )
    
    return HttpResponse("Notification sent!")


def user_notifications(request):
    notifications = request.user.notifications.all()
    return render(request, "notifications/user_notifications.html", {"notifications": notifications})