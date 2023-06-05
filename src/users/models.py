import os
import shutil
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Function for profile pictures path generation:
def profile_picture_upload_to(instance, filename):
    return f"pfps/{instance.user.id}/{filename}"

# Create your models here.
# Profile model:
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_to, blank=True)
    @property
    def username(self):
        return self.user.username
    
    @property
    def email(self):
        return self.user.email

    @property
    def first_name(self):
        return self.user.first_name
    
    @property
    def last_name(self):
        return self.user.last_name
    
    def __str__(self):
        return f"{self.username}'s Profile"

# Making profiles appear for newly created users:
@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Function for deleting profiles on user deletion:
@receiver(post_delete, sender=User)
def delete_profile_for_user(sender, instance, **kwargs):
    try:
        profile = instance.profile
        profile.delete()
    except Profile.DoesNotExist:
        pass

# Function for deleting media directories of profile instances:
@receiver(post_delete, sender=Profile)
def delete_pfp_directory(sender, instance, **kwargs):
    # Construct the path to the directory containing the poster
    directory_path = os.path.dirname(instance.profile_picture.path)

    # Delete the specific film's directory and its contents
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)