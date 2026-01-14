from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any extra fields if needed, e.g. role
    pass

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    # Simple caching fields for stats (optional, but good for performance)
    total_quizzes_taken = models.PositiveIntegerField(default=0)
    # We can calculate average score dynamically or store it here.
    
    def __str__(self):
        return f'{self.user.username} Profile'
