from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # Resume Analyzer
    path('resume-analyzer/', views.resume_analyzer, name='resume_analyzer'),

    # Job Details
    path('job/<int:id>/', views.job_detail, name='job_detail'),

    # Company Details
    path('company/<int:id>/', views.company_detail, name='company_detail'),

    # Apply Job
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    # Applications
    path('my-applications/', views.my_applications, name='my_applications'),

    path(
        'application/<int:pk>/',
        views.application_detail,
        name='application_detail'
    ),

    # Saved Jobs
    path(
        'save-job/<int:id>/',
        views.save_job,
        name='save_job'
    ),

    path(
        'saved-jobs/',
        views.saved_jobs,
        name='saved_jobs'
    ),

    # Resume Upload
    path(
        'upload-resume/',
        views.upload_resume,
        name='upload_resume'
    ),

    path(
        'resumes/',
        views.resume_list,
        name='resume_list'
    ),

    # Resume Analysis
    path(
        'analyze-resume/<int:resume_id>/<int:job_id>/',
        views.analyze_resume,
        name='analyze_resume'
    ),

    # AI Job Matching
    path(
        'best-matching-jobs/<int:id>/',
        views.best_matching_jobs,
        name='best_matching_jobs'
    ),

    # Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # Post Job
    path(
        'post-job/',
        views.post_job,
        name='post_job'
    ),

    # ==================================
    # RECRUITER DASHBOARD
    # ==================================

    path(
        'recruiter-dashboard/',
        views.recruiter_dashboard,
        name='recruiter_dashboard'
    ),

    path(
        'under-review/<int:pk>/',
        views.under_review_application,
        name='under_review_application'
    ),

    path(
        'shortlist/<int:pk>/',
        views.shortlist_application,
        name='shortlist_application'
    ),

    path(
        'schedule-interview/<int:pk>/',
        views.schedule_interview,
        name='schedule_interview'
    ),

    path(
        'select/<int:pk>/',
        views.select_application,
        name='select_application'
    ),

    path(
        'reject/<int:pk>/',
        views.reject_application,
        name='reject_application'
    ),
    path(
    'profile/',
    views.profile,
    name='profile'
),
path(
    'update-profile-picture/',
    views.update_profile_picture,
    name='update_profile_picture'
),
path(
    "job-fit-analyzer/",
    views.job_fit_analyzer,
    name="job_fit_analyzer",
),
path(
    "gemini-test/",
    views.gemini_test,
    name="gemini_test",
),
path(
    "interview/",
    views.interview_home,
    name="interview_home",
),
path(
    "interview/question/",
    views.interview_question,
    name="interview_question",
),
path('interview/report/', views.interview_report, name='interview_report'),
path(
    "interview/finished/",
    views.interview_finished,
    name="interview_finished",
),
path(
    'delete-resume/<int:id>/',
    views.delete_resume,
    name='delete_resume'
),
]