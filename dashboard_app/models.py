import os
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from datetime import datetime
from django.conf import settings
import boto3

# Function to create upload path for media files
def upload_to(instance, filename):
    location_name = instance.item.location.name.replace(" ", "_").lower()
    item_name = instance.item.name.replace(" ", "_").lower()
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'uploads/{location_name}/{item_name}/{current_date}/{filename}'

# Location model
class Location(models.Model):
    geojson = models.TextField()
    description = models.TextField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.description}'

# Item model
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='items')
    geojson = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.location.name}'

# MediaModel for media files related to items
class MediaModel(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='media_files')
    file_url = models.URLField(max_length=500)  # Store the direct URL of the file
    capture_angle = models.FloatField(null=True, blank=True)
    icon_url = models.URLField(max_length=500, null=True, blank=True)
    plot_image_url = models.URLField(max_length=500, null=True, blank=True)  # Store the direct URL of plot images
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item.name} - {self.file_url}'

# Function to delete old file when updating a MediaModel instance
def delete_file_from_s3(file_url):
    if not file_url:
        return
    s3 = boto3.client(
        's3',
        region_name='lon1',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    file_key = file_url.replace(f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/", "")
    s3.delete_object(Bucket=bucket_name, Key=file_key)

# Delete old files when MediaModel is updated
@receiver(pre_save, sender=MediaModel)
def auto_delete_file_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return 
    try:
        old_instance = MediaModel.objects.get(pk=instance.pk)
        # Delete old file and plot image if URLs differ
        if old_instance.file_url != instance.file_url:
            delete_file_from_s3(old_instance.file_url)
        if old_instance.plot_image_url != instance.plot_image_url:
            delete_file_from_s3(old_instance.plot_image_url)
    except MediaModel.DoesNotExist:
        return

# Delete files from S3 when MediaModel is deleted
@receiver(post_delete, sender=MediaModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    delete_file_from_s3(instance.file_url)
    if instance.plot_image_url:
        delete_file_from_s3(instance.plot_image_url)
