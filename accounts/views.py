from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import resend
import logging

logger = logging.getLogger(__name__)


def send_welcome_email(username, email):
    """
    Sends a welcome email using Resend.
    If email sending fails, registration still succeeds.
    """

    try:
        resend.api_key = settings.RESEND_API_KEY

        resend.Emails.send({
            "from": "TalentSyncAI <onboarding@resend.dev>",
            "to": [email],
            "subject": "Welcome to TalentSyncAI",
            "text": f"""
Hello {username},

Welcome to TalentSyncAI!

Your account has been created successfully.

You can now:

• Apply for jobs
• Save jobs
• Upload resumes
• Track applications

Thank you for joining us.

TalentSyncAI Team
""",
        })

        logger.info(
            "Welcome email sent successfully to %s",
            email
        )

    except Exception as e:
        # Email failure will NOT stop user registration
        logger.error(
            "Welcome email failed: %s",
            e
        )


def signup(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        # Check if username already exists
        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "signup.html",
                {
                    "error":
                    "Username already exists."
                }
            )

        # Check if email already exists
        if User.objects.filter(
            email=email
        ).exists():

            return render(
                request,
                "signup.html",
                {
                    "error":
                    "Email is already registered."
                }
            )

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Send welcome email
        # Registration will still succeed
        # if email sending fails
        send_welcome_email(
            username,
            email
        )

        # Redirect after successful registration
        return redirect("home")

    return render(
        request,
        "signup.html"
    )


def user_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect("home")

        return render(
            request,
            "login.html",
            {
                "error":
                "Invalid username or password."
            }
        )

    return render(
        request,
        "login.html"
    )


def user_logout(request):

    logout(request)

    return redirect("home")