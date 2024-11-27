# Generated by Django 5.1.3 on 2024-11-26 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("waste_tracking", "0002_alter_waste_category_alter_waste_weight_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="waste",
            name="collector",
        ),
        migrations.AlterField(
            model_name="waste",
            name="date_collected",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
