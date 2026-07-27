from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import threading


# Send welcome email in the background
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


# User Registration
def signup(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Send welcome email without blocking registration
        threading.Thread(
            target=send_welcome_email,
            args=(username, email),
            daemon=True
        ).start()

        return redirect("home")

    return render(request, "signup.html")


# User Login
def user_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")


# User Logout
def user_logout(request):

    logout(request)

    return redirect("home")