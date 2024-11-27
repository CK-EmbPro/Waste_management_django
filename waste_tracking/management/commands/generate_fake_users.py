from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Generate fake users'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Number of users to generate
        number_of_users = 500000

        # Start generating users
        for _ in range(number_of_users):
            # Generate a fake username
            username = fake.user_name()

            # Ensure the username is unique by checking the database
            while CustomUser.objects.filter(username=username).exists():
                username = fake.user_name()  # If the username exists, generate a new one

            # Generate other fake data
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            password = fake.password()
            phone_number = fake.phone_number()
            role = fake.random_element(elements=('collector', 'normal_user'))

            # Create the user
            try:
                # Create the CustomUser object
                CustomUser.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    phone_number=phone_number,
                    role=role
                )
            except IntegrityError:
                # Skip user creation if unique constraints are violated (username or email)
                continue

        # After all users are created
        self.stdout.write(self.style.SUCCESS('Successfully generated 500,000 users.'))
