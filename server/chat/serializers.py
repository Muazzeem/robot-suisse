from rest_framework import serializers

class OutputSerializer(serializers.Serializer):
    company = serializers.CharField()
    question = serializers.CharField()
    output = serializers.CharField()
    uid = serializers.CharField()


