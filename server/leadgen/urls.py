from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps import Sitemap as WagtailSitemap

from search import views as search_views
from .wagtail_api import api_router


def robots_txt(request):
    sitemap_url = f"{settings.BACKEND_HOST}/sitemap.xml"
    text = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /django-admin/",
        "Disallow: /account/",
        "Disallow: /documents/",
        "Disallow: /media/",
        "Disallow: /static/",
        "Disallow: /api/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(text), content_type="text/plain")


sitemaps = {
    'wagtail': WagtailSitemap,
}

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("api/v2/", api_router.urls),
    path("api/v1/home/", include("home.urls", namespace="home")),
    path("api/v1/utility/", include("utility.urls", namespace="utility")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("", include(wagtail_urls)),
]