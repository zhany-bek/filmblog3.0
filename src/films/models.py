import os
import shutil
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete


def poster_upload_to(instance, filename):
    adjusted_title = instance.title.replace(' ', '_').lower()
    return f"posters/{adjusted_title}_{instance.release_year}/{filename}"

# Create your models here.
class Film(models.Model):
    title = models.CharField(max_length=100)
    director_name = models.CharField(max_length=100, null=True)
    release_year = models.PositiveIntegerField(null=True)
    poster = models.ImageField(upload_to=poster_upload_to, blank=True, null=True)
    description = models.TextField(blank=True)
    rating = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        self.title = self.title.replace(' ', '_').lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}_{self.release_year}"

# Function for deleting the media directory of the deleted film instance:
@receiver(post_delete, sender=Film)
def delete_poster_directory(sender, instance, **kwargs):
    # Construct the path to the directory containing the poster
    if instance.poster:
        directory_path = os.path.dirname(instance.poster.path)

    # Delete the specific film's directory and its contents
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)