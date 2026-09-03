from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    #   One-to-One relationship with User
      user = models.OneToOneField(
          User,
          on_delete=models.CASCADE,
          related_name='profile'
      )
      bio = models.TextField(blank=True)
      location = models.CharField(max_length=100, blank=True)
      birth_date = models.DateField(null=True, blank=True)
      phone = models.CharField(max_length=15, blank=True)
      profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
      
      def __str__(self):
          return f"{self.user.username}'s Profile"