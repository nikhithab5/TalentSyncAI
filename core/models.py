from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Company(models.Model):

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    website = models.URLField()
    description = models.TextField()
    logo = CloudinaryField(

    'logo',
    blank=True,
    null=True
)

    def __str__(self):
        return self.name

class Job(models.Model):

    title = models.CharField(max_length=100)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    description = models.TextField()
    skills = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Application(models.Model):

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    INTERVIEW_MODE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    applied_on = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    interview_date = models.DateField(
        null=True,
        blank=True
    )

    interview_time = models.TimeField(
        null=True,
        blank=True
    )

    interview_mode = models.CharField(
        max_length=20,
        choices=INTERVIEW_MODE_CHOICES,
        null=True,
        blank=True
    )

    meeting_link = models.URLField(
        null=True,
        blank=True
    )

    recruiter_notes = models.TextField(
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"

    class Meta:
        ordering = ['-applied_on']

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'job'],
                name='unique_job_application'
            )
        ]


class SavedJob(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    saved_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"


class Resume(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    resume = models.FileField(
        upload_to='resumes/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-uploaded_at']
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    tsa_id = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True
    )

    image = models.ImageField(
        default='profile_pics/default.png',
        upload_to='profile_pics'
    )

    def __str__(self):
        return f"{self.user.username} Profile"
    
class InterviewResult(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    job_role = models.CharField(
        max_length=100
    )

    question = models.TextField()

    answer = models.TextField()

    feedback = models.TextField()

    score = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.job_role}"