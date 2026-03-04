from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Company
from .serializers import CompanySerializer

class CompanyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100  


class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.prefetch_related('contact_persons').all()
    serializer_class = CompanySerializer
    pagination_class = CompanyPagination

