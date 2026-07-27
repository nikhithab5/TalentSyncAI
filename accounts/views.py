from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import threading


def send_welcome_email(username, email):
    try:
        send_mail(
            subject="Welcome to TalentSyncAI",
            message=f"""
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
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )
    except Exception:
        pass


def signup(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        # Check required fields
        if not username or not email or not password:
            return render(
                request,
                "signup.html",
                {
                    "error": "All fields are required."
                }
            )

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "signup.html",
                {
                    "error": "Username already exists. Please choose another username."
                }
            )

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(
                request,
                "signup.html",
                {
                    "error": "Email already registered. Please use another email."
                }
            )

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Send welcome email in background
        # This will NOT block the signup process
        threading.Thread(
            target=send_welcome_email,
            args=(username, email),
            daemon=True
        ).start()

        # Redirect immediately after successful registration
        return redirect("home")

    return render(request, "signup.html")


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "login.html")


def user_logout(request):

    logout(request)

    return redirect("home")