from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "place",
            "time",
            "action",
            "is_reward",
            "related",
            "reward_text",
            "frequency",
            "duration_seconds",
            "is_public",
        ]

    def validate(self, data):
        if data.get("related") and data.get("reward_text"):
            raise serializers.ValidationError(
                "Укажите либо related, либо reward_text, но не оба."
            )
        if (data.get("is_reward")
                and (data.get("related") or data.get("reward_text"))):

            raise serializers.ValidationError(
                "Приятная привычка не должна иметь related/reward."
            )
        if data.get("duration_seconds", 0) > 120:
            raise serializers.ValidationError(
                "duration_seconds не более 120 сек.")
        freq = data.get("frequency", 1)
        if not (1 <= freq <= 7):
            raise serializers.ValidationError(
                "frequency в диапазоне 1–7 дней.")
        return data
