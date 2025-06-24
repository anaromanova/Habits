from rest_framework import viewsets, permissions, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Habit
from .serializers import HabitSerializer

class FivePerPagePagination(pagination.PageNumberPagination):
    page_size = 5

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = FivePerPagePagination

    def get_permissions(self):
        if self.action == 'list_public':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.action == 'list_public':
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='public')
    def list_public(self, request):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

