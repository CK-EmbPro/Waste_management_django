from django.db import models
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class Waste(models.Model):
    
    WASTE_CATEGORIES = (
        ('biodegradable', 'Biodegradable'),
        ('non_biodegradable', 'Non_biodegradable')
    )
    
    category = models.CharField(max_length=20, choices=WASTE_CATEGORIES)
    weight = models.FloatField(help_text="kgs")
    date_collected = models.DateField(default=datetime.date.today)
    description = models.TextField(blank=True)
    is_collected = models.BooleanField(default=False)