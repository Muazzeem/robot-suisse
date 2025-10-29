from django.urls import path
from .views import AllSettingsAPIView

app_name = "utility"

urlpatterns = [
    path("", AllSettingsAPIView.as_view(), name="all-settings"),
]
