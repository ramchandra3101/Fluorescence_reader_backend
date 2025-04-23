# geminiapp/serializers.py
from rest_framework import serializers
from .models import GeminiProcessedImage

class GeminiProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeminiProcessedImage
        fields = ['id', 'image', 'processed_image', 'result_json', 'created_at']
        read_only_fields = ['result_json', 'created_at']