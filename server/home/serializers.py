from rest_framework import serializers

from .models import BlogCategoryPage


class BlogCategoryPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategoryPage
        fields = ("id", "title", "title_ar", "slug")
