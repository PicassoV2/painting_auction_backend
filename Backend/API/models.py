from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_painter = models.BooleanField(default=False)  # Whether the user is a painter
    is_painter_requested = models.BooleanField(default=False)  # Painter request status
    is_painter_approved = models.BooleanField(default=False)  # Add this field


    def __str__(self):
        return self.user.username

# API/models.py
class Painting(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='paintings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='paintings/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
