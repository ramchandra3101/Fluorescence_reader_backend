from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serailizers import Imageprocessing_Serializer
from .services.ImageProcessor import ImageProcessor
from .services.JsonFormatter import JSONFormatter
import os
from django.conf import settings
import cv2
from django.core.files.base import ContentFile
import io
from PIL import Image
import base64


# Create your views here.
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def process_image(request):
    serializer = Imageprocessing_Serializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        try:
            image_processor = ImageProcessor()
            image_path = os.path.join(settings.MEDIA_ROOT, instance.image.name)
            result_json, contoured_image = image_processor.process_image(image_path)
            
            # Convert numpy array to file-like object
            success, buffer = cv2.imencode('.jpg', contoured_image)
            if not success:
                raise ValueError("Failed to encode the contoured image")
            
            # Save the image to the processed_image field
            content_file = ContentFile(buffer.tobytes())
            instance.result_json = result_json
            instance.processed_image.save(f"processed_{os.path.basename(instance.image.name)}", content_file, save=True)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            return Response(
                {
                    'id': instance.id,
                    'image': instance.image.url,
                    'processed_image': image_base64,
                    'result_json': instance.result_json,
                    'created_at': instance.created_at
                },
                status= status.HTTP_201_CREATED
            )
        except Exception as e:
            instance.delete()
            return Response(
                {
                    'error': str(e)
                },
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
