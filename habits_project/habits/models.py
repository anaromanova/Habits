from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_reward = models.BooleanField(default=False)
    related = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        limit_choices_to={'is_reward': True}, related_name='reward_for'
    )
    reward_text = models.CharField(max_length=255, blank=True)
    frequency = models.PositiveIntegerField(default=1)          # дни (1–7)
    duration_seconds = models.PositiveIntegerField(default=60)  # ≤120
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.related and self.reward_text:
            raise ValidationError("Укажите либо related, либо reward_text, но не оба.")
        if self.is_reward and (self.related or self.reward_text):
            raise ValidationError("Приятная привычка не должна иметь related или вознаграждение.")
        if self.duration_seconds > 120:
            raise ValidationError("duration_seconds не более 120 сек.")
        if not (1 <= self.frequency <= 7):
            raise ValidationError("frequency в диапазоне 1–7 дней.")
        super().clean()

    def __str__(self):
        return f"{self.action} @ {self.time.strftime('%H:%M')} в {self.place}"

