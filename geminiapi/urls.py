# geminiapp/urls.py
from django.urls import path
from .views import process_image_with_gemini

urlpatterns = [
    path('process', process_image_with_gemini, name='process_image_with_gemini'),
]