from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse



def signup(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        send_mail(
            subject='Welcome to TalentSyncAI',
            message=f'''
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
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('home')

    return render(request, 'signup.html')



def user_login(request):
    try:
        return render(request, "login.html")
    except Exception as e:
        import traceback
        return HttpResponse(
            "<pre>" + traceback.format_exc() + "</pre>",
            content_type="text/html"
        )
def user_logout(request):

    logout(request)

    return redirect('home')