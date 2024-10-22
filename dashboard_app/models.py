import os
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from datetime import datetime

# Fonction pour créer le chemin de téléchargement pour les fichiers multimédias
def upload_to(instance, filename):
    location_name = instance.item.location.name.replace(" ", "_").lower()
    item_name = instance.item.name.replace(" ", "_").lower()
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'uploads/{location_name}/{item_name}/{current_date}/{filename}'

# Fonction pour créer le chemin de téléchargement pour les images de graphique
def upload_plot_to(instance, filename):
    location_name = instance.item.location.name.replace(" ", "_").lower()
    item_name = instance.item.name.replace(" ", "_").lower()
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f'uploads/{location_name}/{item_name}/{current_date}/plots/{filename}'

class Location(models.Model):
    geojson = models.TextField()
    description = models.TextField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.name} - {self.description}'

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='items')
    geojson = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name} - {self.location.name}'

class MediaModel(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to=upload_to)
    capture_angle = models.FloatField(null=True, blank=True)
    icon_url = models.URLField(max_length=500, null=True, blank=True)
    plot_image = models.ImageField(upload_to=upload_plot_to, null=True, blank=True)  # Stocker l'image du graphique ici
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.item} - {self.file}'


# Suppression des anciens fichiers lors de la mise à jour
def delete_old_file(instance):
    if instance and instance.file:
        file_path = instance.file.path
        if os.path.isfile(file_path):
            os.remove(file_path)

# Suppression des anciens fichiers lors de la suppression du modèle MediaModel
@receiver(pre_save, sender=MediaModel)
def auto_delete_file_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return 
    try:
        old_instance = MediaModel.objects.get(pk=instance.pk)
        old_file = old_instance.file
    except MediaModel.DoesNotExist:
        return

    if old_file and old_file != instance.file:
        delete_old_file(old_instance)

@receiver(post_delete, sender=MediaModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        delete_old_file(instance)