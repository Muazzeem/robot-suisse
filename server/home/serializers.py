from rest_framework import serializers
from home.fields import ImageSerializerField

from .models import BlogCategoryPage


class BlogCategoryPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategoryPage
        fields = ("id", "title", "title_ar", "slug")
