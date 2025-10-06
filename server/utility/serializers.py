from rest_framework import serializers

from .models import ContactUs, Subscribe, Service


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title", "subtitle", "icon_image", "detail_page_link", "description"]
