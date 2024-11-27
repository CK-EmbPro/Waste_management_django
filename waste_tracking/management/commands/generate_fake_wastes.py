from django.core.management.base import BaseCommand
from faker import Faker
from waste_tracking.models import Waste
import random
from datetime import datetime

class Command(BaseCommand):
    help = 'Generates 500,000 rows of waste data and saves it in the database'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Define the batch size for saving to the database
        batch_size = 1000
        
        # WASTE_CATEGORIES to choose from
        categories = ['biodegradable', 'non_biodegradable']
        
        # List to hold waste data
        waste_data = []
        
        # Default values for NULL replacement
        default_description = "No description available"
        default_weight = 1.0  # Default weight in case the generated value is NULL or invalid
        
        # Generate 500,000 records
        for _ in range(500000):
            # Generate random data
            category = random.choice(categories)
            weight = round(random.uniform(1, 100), 2)  # Random weight between 1kg and 100kg
            date_collected = fake.date_this_year()  # Random date within the current year
            description = fake.text(max_nb_chars=200)  # Random description

            # Check and replace NULL values (or empty values) for each field
            if not description:  # Replace NULL or empty description with the default
                description = default_description
            
            if weight is None or weight <= 0:  # Replace NULL or invalid weight
                weight = default_weight

            # Append the new waste data record to the list
            waste_data.append(
                Waste(
                    category=category,
                    weight=weight,
                    date_collected=date_collected,
                    description=description
                )
            )
            
            # Save the data in batches to avoid memory issues
            if len(waste_data) >= batch_size:
                Waste.objects.bulk_create(waste_data)
                waste_data.clear()  # Clear the list for the next batch
                
        # Save any remaining data that hasn't been saved
        if waste_data:
            Waste.objects.bulk_create(waste_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully generated 500,000 waste records.'))
