from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .views import *

app_name = "home"

public_router = DefaultRouter()
# public_router.register(r"blogs", BlogApiViewset, "public_blog_api")


urlpatterns = [
    path("public/", include(public_router.urls)),
]
