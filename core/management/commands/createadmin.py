from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = "Create admin user if it doesn't exist"

    def handle(self, *args, **kwargs):

        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")
        email = os.getenv("ADMIN_EMAIL")

        if not username or not password or not email:
            self.stdout.write(
                self.style.ERROR(
                    "Missing ADMIN_USERNAME, ADMIN_PASSWORD or ADMIN_EMAIL"
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f"Admin '{username}' already exists.")
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Superuser '{username}' created successfully.")
        )