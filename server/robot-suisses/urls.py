from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from .wagtail_api import api_router

# ------------------------------------------------------------
# Non-translatable (language-neutral) URLs
# ------------------------------------------------------------
urlpatterns = [
    path("django-admin/", admin.site.urls),  # Django admin
    path("admin/", include(wagtailadmin_urls)),  # Wagtail admin
    path("documents/", include(wagtaildocs_urls)),  # Wagtail documents
    path("api/v2/", api_router.urls),  # Wagtail API (headless)
    path("api/v1/home/", include("home.urls", namespace="home")),
    path("api/v1/utility/", include("utility.urls", namespace="utility")),
]

# ------------------------------------------------------------
# Translatable (locale-aware) URLs
# ------------------------------------------------------------
urlpatterns += i18n_patterns(
    # Any page or view that should vary by language goes here
    path("search/", search_views.search, name="search"),
    path("", include(wagtail_urls)),  # Wagtail site pages
    prefix_default_language=False,    # Keeps default locale clean (optional)
)

# ------------------------------------------------------------
# Static + Media files (for dev mode)
# ------------------------------------------------------------
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
