from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telegram_chat_id = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"Profile({self.user.username})"
