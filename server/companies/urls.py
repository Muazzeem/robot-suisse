from django.urls import path
from .views import CompanyListAPIView

app_name = 'companies'

urlpatterns = [
    path('', CompanyListAPIView.as_view(), name='company-list'),
]