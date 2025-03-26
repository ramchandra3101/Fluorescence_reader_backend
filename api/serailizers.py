from rest_framework import serializers
from .models import ProcessedImage

class Imageprocessing_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedImage
        fields = ['id', 'image', 'processed_image', 'result_json', 'created_at']
        read_only_fields = ['processed_image', 'result_json', 'created_at']


    




