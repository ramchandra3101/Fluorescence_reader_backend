from django.db import models

# Create your models here.

class ProcessedImage(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    processed_image = models.ImageField(upload_to='processed/%Y/%m/%d/', null=True, blank=True)
    result_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Processed Image {self.id}-{self.created_at}"


    


    