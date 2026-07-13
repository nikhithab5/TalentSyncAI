from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "login",
            "signup",
            "dashboard",
            "upload_resume",
            "resume_list",
            "saved_jobs",
            "my_applications",
            "job_fit_analyzer",
            "interview_home",
            "profile",
        ]

    def location(self, item):
        return reverse(item)