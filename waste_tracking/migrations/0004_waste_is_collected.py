# Generated by Django 5.1.3 on 2024-11-26 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("waste_tracking", "0003_remove_waste_collector_alter_waste_date_collected"),
    ]

    operations = [
        migrations.AddField(
            model_name="waste",
            name="is_collected",
            field=models.BooleanField(default=False),
        ),
    ]
