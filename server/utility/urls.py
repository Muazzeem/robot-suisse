from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "utility"

public_router = DefaultRouter()
public_router.register(r"contact-us", ContactUsApiViewset, "public_contact_us_api")
public_router.register(r"subscribe", SubscribeApiViewset, "public_subscribe_api")


urlpatterns = [
    path("public/", include(public_router.urls)),
    path("search/", search_services, name="search-services"),
]
