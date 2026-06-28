from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Company, Job, Application, SavedJob, Resume
from .forms import ResumeForm, JobForm
import PyPDF2
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    query = request.GET.get('q')

    if query:
        jobs = Job.objects.filter(title__icontains=query)
    else:
        jobs = Job.objects.all()

    return render(request, 'home.html', {
        'jobs': jobs
    })


def resume_analyzer(request):
    return render(request, 'resume_analyzer.html')


def job_detail(request, id):

    job = get_object_or_404(Job, id=id)
    resumes = Resume.objects.all()

    return render(request, 'job_detail.html', {
        'job': job,
        'resumes': resumes
    })


def company_detail(request, id):

    company = get_object_or_404(Company, id=id)

    jobs = Job.objects.filter(company=company)

    return render(request, 'company_detail.html', {
        'company': company,
        'jobs': jobs
    })
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def apply_job(request, job_id):

    job = Job.objects.get(id=job_id)

    Application.objects.get_or_create(
        user=request.user,
        job=job
    )

    send_mail(
        subject='Application Submitted Successfully',

        message=f'''
Hello {request.user.username},

Your application for "{job.title}" at "{job.company.name}" has been submitted successfully.

Our recruitment team will review your application and update you on the next steps.

Thank you for using TalentSync AI.

Best Regards,
TalentSync AI Team
''',

        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
        fail_silently=False,
    )

    messages.success(
        request,
        "Application submitted successfully."
    )

    return redirect('home')
@login_required
def my_applications(request):

    applications = Application.objects.filter(
        user=request.user
    )

    return render(
        request,
        'my_applications.html',
        {
            'applications': applications
        }
    )

@login_required
def save_job(request, id):

    job = get_object_or_404(Job, id=id)

    SavedJob.objects.get_or_create(
        user=request.user,
        job=job
    )

    return redirect('saved_jobs')


@login_required
def saved_jobs(request):

    jobs = SavedJob.objects.filter(
        user=request.user
    )

    return render(request, 'saved_jobs.html', {
        'jobs': jobs
    })


from django.contrib.auth.decorators import login_required

@login_required
def upload_resume(request):

    if request.method == 'POST':

        form = ResumeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            return redirect('resume_list')

    else:
        form = ResumeForm()

    return render(
        request,
        'upload_resume.html',
        {
            'form': form
        }
    )

@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)

    return render(
        request,
        'resume_list.html',
        {
            'resumes': resumes
        }
    )
def analyze_resume(request, resume_id, job_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id
    )

    job = get_object_or_404(
        Job,
        id=job_id
    )

    pdf_file = open(
        resume.resume.path,
        'rb'
    )

    reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    required_skills = [
        skill.strip()
        for skill in job.skills.split(',')
    ]

    found_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.lower() in text.lower():
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = int(
        (len(found_skills) / len(required_skills)) * 100
    )

    return render(
        request,
        'resume_analysis.html',
        {
            'resume': resume,
            'job': job,
            'score': score,
            'found_skills': found_skills,
            'missing_skills': missing_skills
        }
    )


def best_matching_jobs(request, id):

    resume = get_object_or_404(
        Resume,
        id=id
    )

    pdf_file = open(
        resume.resume.path,
        'rb'
    )

    reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    jobs = Job.objects.all()

    results = []

    for job in jobs:

        required_skills = [
            skill.strip()
            for skill in job.skills.split(',')
        ]

        found = 0

        for skill in required_skills:

            if skill.lower() in text.lower():
                found += 1

        score = int(
            (found / len(required_skills)) * 100
        )

        results.append({
            'job': job,
            'score': score
        })

    results = sorted(
        results,
        key=lambda x: x['score'],
        reverse=True
    )

    return render(
        request,
        'best_matching_jobs.html',
        {
            'resume': resume,
            'results': results
        }
    )


def dashboard(request):

    total_jobs = Job.objects.count()
    total_resumes = Resume.objects.count()
    total_saved_jobs = SavedJob.objects.count()
    total_applications = Application.objects.count()

    return render(
        request,
        'dashboard.html',
        {
            'total_jobs': total_jobs,
            'total_resumes': total_resumes,
            'total_saved_jobs': total_saved_jobs,
            'total_applications': total_applications,
        }
    )


def post_job(request):

    if request.method == 'POST':

        form = JobForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect('home')

    else:

        form = JobForm()

    return render(
        request,
        'post_job.html',
        {
            'form': form
        }
    )
# =====================================================
# APPLICATION DETAILS
# =====================================================

@login_required
def application_detail(request, pk):

    application = get_object_or_404(
        Application,
        id=pk,
        user=request.user
    )

    return render(
        request,
        'application_detail.html',
        {
            'application': application
        }
    )


# =====================================================
# RECRUITER DASHBOARD
# =====================================================

@login_required
def recruiter_dashboard(request):

    applications = Application.objects.all().order_by(
        '-applied_on'
    )

    shortlisted_count = Application.objects.filter(
        status='Shortlisted'
    ).count()

    selected_count = Application.objects.filter(
        status='Selected'
    ).count()

    rejected_count = Application.objects.filter(
        status='Rejected'
    ).count()

    return render(
        request,
        'recruiter_dashboard.html',
        {
            'applications': applications,
            'shortlisted_count': shortlisted_count,
            'selected_count': selected_count,
            'rejected_count': rejected_count,
        }
    )


# =====================================================
# MOVE TO UNDER REVIEW
# =====================================================

@login_required
def under_review_application(request, pk):

    application = get_object_or_404(
        Application,
        id=pk
    )

    application.status = "Under Review"
    application.save()

    return redirect(
        'recruiter_dashboard'
    )


# =====================================================
# SHORTLIST APPLICATION
# =====================================================

@login_required
def shortlist_application(request, pk):

    application = get_object_or_404(
        Application,
        id=pk
    )

    application.status = "Shortlisted"
    application.save()

    return redirect(
        'recruiter_dashboard'
    )


# =====================================================
# SCHEDULE INTERVIEW
# =====================================================

@login_required
def schedule_interview(request, pk):

    application = get_object_or_404(
        Application,
        id=pk
    )

    if request.method == "POST":

        application.status = "Interview Scheduled"

        application.interview_date = request.POST.get(
            "interview_date"
        )

        application.interview_time = request.POST.get(
            "interview_time"
        )

        application.interview_mode = request.POST.get(
            "interview_mode"
        )

        application.meeting_link = request.POST.get(
            "meeting_link"
        )

        application.save()

        return redirect(
            'recruiter_dashboard'
        )

    return render(
        request,
        'schedule_interview.html',
        {
            'application': application
        }
    )


# =====================================================
# SELECT APPLICATION
# =====================================================

@login_required
def select_application(request, pk):

    application = get_object_or_404(
        Application,
        id=pk
    )

    application.status = "Selected"
    application.save()

    return redirect(
        'recruiter_dashboard'
    )


# =====================================================
# REJECT APPLICATION
# =====================================================

@login_required
def reject_application(request, pk):

    application = get_object_or_404(
        Application,
        id=pk
    )

    application.status = "Rejected"
    application.save()

    return redirect(
        'recruiter_dashboard'
    )
@login_required
def profile(request):

    applications = Application.objects.filter(
        user=request.user
    ).count()

    saved_jobs = SavedJob.objects.filter(
        user=request.user
    ).count()

    resumes = Resume.objects.filter(
        user=request.user
    ).count()

    context = {
        'applications': applications,
        'saved_jobs': saved_jobs,
        'resumes': resumes,
    }

    return render(
        request,
        'profile.html',
        context
    )
from django.contrib.auth.decorators import login_required

@login_required
def update_profile_picture(request):

    if request.method == "POST":

        profile = request.user.profile

        if 'image' in request.FILES:
            profile.image = request.FILES['image']
            profile.save()

        return redirect('profile')

    return render(
        request,
        'update_profile_picture.html'
    )
@login_required
def analyze_job(request):

    if request.method == "POST":

        job_description = request.POST.get("job_description")

        found_skills = []

        for skill in SKILLS_DATABASE:

            if skill.lower() in job_description.lower():
                found_skills.append(skill)

        return render(
            request,
            "analyze_job.html",
            {
                "job_description": job_description,
                "found_skills": found_skills,
            },
        )

    return render(request, "analyze_job.html")

@login_required
def job_fit_analyzer(request):

    resume = Resume.objects.filter(
        user=request.user
    ).order_by('-id').first()

    score = None
    found_skills = []
    missing_skills = []

    if request.method == "POST" and resume:

        job_description = request.POST.get(
            "job_description",
            ""
        )

        pdf_file = open(
            resume.resume.path,
            "rb"
        )

        reader = PyPDF2.PdfReader(
            pdf_file
        )

        resume_text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                resume_text += page_text

        common_skills = [
            "python",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "sql",
            "nlp",
            "docker",
            "aws",
            "git",
            "pandas",
            "numpy",
            "scikit-learn"
        ]

        for skill in common_skills:

            if skill.lower() in job_description.lower():

                if skill.lower() in resume_text.lower():
                    found_skills.append(skill)
                else:
                    missing_skills.append(skill)

        total = len(found_skills) + len(missing_skills)

        if total > 0:
            score = int(
                len(found_skills) / total * 100
            )
        else:
            score = 0

    return render(
        request,
        "job_fit_analyzer.html",
        {
            "resume": resume,
            "score": score,
            "found_skills": found_skills,
            "missing_skills": missing_skills
        }
    )