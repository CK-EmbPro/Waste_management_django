from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    
    title = models.CharField(
        max_length=255,
    )
    
    message= models.TextField()
    
    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES,
        default='info'
    )
    
    is_read = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user.username}:{self.title}"
    
    
    def mark_as_read(self):
        """Marks the notification as read"""
        self.is_read = True
        self.save()