from django.contrib import admin
from .models import Notification
# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('is_read', 'notification_type', 'created_at')
    search_fields= ('title', 'message', 'user__username')