# geminiapp/models.py
from django.db import models


class GeminiProcessedImage(models.Model):
    image = models.ImageField(upload_to='gemini_uploads/%Y/%m/%d/')
    processed_image = models.ImageField(upload_to='gemini_processed/%Y/%m/%d/', null=True, blank=True)
    result_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gemini Processed Image {self.id}-{self.created_at}"