from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins


from .serializers import *
from .models import ContactUs, Service


class ContactUsApiViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()

class SubscribeApiViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()


@api_view(["GET"])
def search_services(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return Response([])

    results = Service.objects.filter(title__icontains=query)[:10]
    serializer = ServiceSerializer(results, many=True)
    return Response(serializer.data)

