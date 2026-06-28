from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Company,
    Job,
    Application,
    SavedJob,
    Resume,
    Profile
)


# -------------------------
# Company Admin
# -------------------------

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'website',
    )

    search_fields = (
        'name',
        'location',
    )


# -------------------------
# Job Admin
# -------------------------

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'company',
        'location',
        'salary',
        'created_at',
    )

    search_fields = (
        'title',
        'company__name',
        'location',
    )

    list_filter = (
        'company',
        'location',
    )

    ordering = ('-created_at',)


# -------------------------
# Saved Jobs
# -------------------------

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'job',
        'saved_on',
    )


# -------------------------
# Resume Admin
# -------------------------

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'uploaded_at',
    )


# -------------------------
# Profile Admin
# -------------------------

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'tsa_id',
        'user',
        'email',
        'image',
    )

    search_fields = (
        'tsa_id',
        'user__username',
        'user__email',
    )

    readonly_fields = (
        'tsa_id',
    )

    ordering = (
        'tsa_id',
    )

    def email(self, obj):
        return obj.user.email


# -------------------------
# Application Admin
# -------------------------

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'job',
        'status',
        'interview_date',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'user__username',
        'job__title',
    )

    def save_model(self, request, obj, form, change):

        super().save_model(request, obj, form, change)

        # Interview Scheduled Email
        if obj.status == 'Interview Scheduled':

            send_mail(
                subject='Interview Invitation - TalentSync AI',
                message=f"""
Hello {obj.user.username},

Congratulations!

You have been shortlisted for:

{obj.job.title}

Interview Details

Date: {obj.interview_date}
Time: {obj.interview_time}
Mode: {obj.interview_mode}

Meeting Link:
{obj.meeting_link}

Please join 10 minutes before the interview.

Best Regards,
TalentSync AI Recruitment Team
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.user.email],
                fail_silently=False,
            )

        elif obj.status == 'Selected':

            send_mail(
                subject='Congratulations! You Have Been Selected',
                message=f"""
Hello {obj.user.username},

Congratulations!

You have been selected for:

{obj.job.title}

Our HR team will contact you shortly.

Best Regards,
TalentSync AI Recruitment Team
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.user.email],
                fail_silently=False,
            )

        elif obj.status == 'Rejected':

            send_mail(
                subject='Application Update - TalentSync AI',
                message=f"""
Hello {obj.user.username},

Thank you for applying for:

{obj.job.title}

After careful consideration, we have decided to move forward with other candidates.

We appreciate your interest and encourage you to apply again.

Best Regards,
TalentSync AI Recruitment Team
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.user.email],
                fail_silently=False,
            )