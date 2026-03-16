from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_CHOICES = [
        ('disease', 'Disease Alert'),
        ('weather', 'Weather Alert'),
        ('advisory', 'Advisory Message'),
        ('general', 'General Notification'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    # If we want to send to all farmers, we can leave recipient null or use a ManyToMany
    # For now, let's allow targeting all or specific users
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)

    def __str__(self):
        return self.title
