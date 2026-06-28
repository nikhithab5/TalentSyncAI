from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

print("✅ Signals file loaded successfully")


@receiver(user_logged_in)
def send_login_email(request, user, **kwargs):

    print("🔥 Login signal triggered")
    print("👤 Username:", user.username)
    print("📧 User Email:", user.email)

    if user.email:
        try:
            result = send_mail(
                'Login Alert - TalentSync AI',

                f'''
Hello {user.username},

You have successfully logged in to TalentSync AI.

If this was not you, please secure your account immediately.

Thank you,
TalentSync AI Team
                ''',

                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            print("📨 send_mail() returned:", result)
            print("✅ Email sent successfully")

        except Exception as e:
            print("❌ Error sending email:", e)