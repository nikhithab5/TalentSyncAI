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
    Registration will continue even if email sending fails.
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

        # Do NOT strip passwords
        password = request.POST.get(
            "password",
            ""
        )

        # Check username
        if not username:
            return render(
                request,
                "signup.html",
                {
                    "error": "Username is required.",
                    "username": username,
                    "email": email,
                },
            )

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "signup.html",
                {
                    "error": "Username already exists.",
                    "username": username,
                    "email": email,
                },
            )

        # Check email
        if not email:
            return render(
                request,
                "signup.html",
                {
                    "error": "Email is required.",
                    "username": username,
                    "email": email,
                },
            )

        if User.objects.filter(
            email=email
        ).exists():

            return render(
                request,
                "signup.html",
                {
                    "error": "Email is already registered.",
                    "username": username,
                    "email": email,
                },
            )

        # Check password
        if not password:
            return render(
                request,
                "signup.html",
                {
                    "error": "Password is required.",
                    "username": username,
                    "email": email,
                },
            )

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        # Send welcome email
        send_welcome_email(
            username,
            email
        )

        # After registration, go to LOGIN page
        return redirect("login")

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

        # Do NOT strip password
        password = request.POST.get(
            "password",
            ""
        )

        print("========== LOGIN ATTEMPT ==========")
        print("Username:", username)

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            print(
                "Login Successful:",
                user.username
            )

            # Explicit backend because your project
            # has multiple authentication backends
            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )

            return redirect("home")

        print("Authentication Failed")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid username or password.",
                "username": username,
            },
        )

    return render(
        request,
        "login.html"
    )


def user_logout(request):

    logout(request)

    return redirect("home")

