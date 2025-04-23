# geminiapp/views.py
import os
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import GeminiProcessingSerializer
from .models import GeminiProcessedImage
from .services.gemini_processor import GeminiImageProcessor

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def process_image_with_gemini(request):
    serializer = GeminiProcessingSerializer(data=request.data)
    
    if serializer.is_valid():
        instance = serializer.save()
        try:
            # Process the image with Gemini
            image_processor = GeminiImageProcessor()
            image_path = os.path.join(settings.MEDIA_ROOT, instance.image.name)
            print(f"Processing image at: {image_path}")
            result_json = image_processor.process_image(image_path)
            
            # Save the result
            instance.result_json = result_json
            instance.save()
            
            return Response(
                {
                    'id': instance.id,
                    'image': instance.image.url,
                    'result_json': instance.result_json,
                    'created_at': instance.created_at
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # Delete the instance if processing fails
            instance.delete()
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)