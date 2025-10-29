from rest_framework import serializers
from .models import Author
from .fields import ImageSerializerField 

class AuthorSerializer(serializers.ModelSerializer):
    image = ImageSerializerField()

    class Meta:
        model = Author
        fields = "__all__"