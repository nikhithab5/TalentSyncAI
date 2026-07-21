from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from core.sitemaps import StaticViewSitemap
from core.views import robots_txt


# -------- TalentSync AI Admin Branding --------

admin.site.site_header = "TalentSync AI Administration"
admin.site.site_title = "TalentSync AI Admin Portal"
admin.site.index_title = "Welcome to TalentSync AI Dashboard"


sitemaps = {
    "static": StaticViewSitemap,
}


urlpatterns = [
    path("robots.txt", robots_txt),

    path("admin/", admin.site.urls),

    path("", include("core.urls")),

    path("accounts/", include("accounts.urls")),

    path("accounts/", include("allauth.urls")),

    # Password reset URLs
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )