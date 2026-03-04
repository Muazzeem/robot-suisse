from rest_framework import serializers
from .models import Company, ContactPerson

class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = [
            "name",
            "job_title",
            "email",
            "phone",
            "avatar",
            "last_updated",
        ]

class CompanySerializer(serializers.ModelSerializer):
    contact_persons = ContactPersonSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = [
            "link",
            "slug",
            "name",
            "source_page",
            "is_detail_fetched",
            "last_updated",
            "banner_image",
            "logo",
            "detail_country",
            "detail_type",
            "detail_employees",
            "description",
            "address",
            "email",
            "phone",
            "website",
            "contact_persons",
        ]
