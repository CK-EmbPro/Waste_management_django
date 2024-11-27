from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        
        ('collector', 'Collector'),
        ('normal_user', 'Normal user'),
    )
    
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='normal_user')
    
    groups =models.ManyToManyField(
        Group, 
        related_name="customuser_groups",
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission, 
        related_name="customuser_permissions",
        blank=True
    )
    
    def is_collector(self):
        return self.role=='collector'
    
    def __str__(self):
        return self.username