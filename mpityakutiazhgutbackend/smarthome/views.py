from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Appliance, ApplianceCategory, Room, AirConditioner
from .serializers import ApplianceSerializer, ApplianceCategorySerializer, RoomSerializer, AirConditionerSerializer
from django.utils import timezone
import datetime
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperUserOrReadOnly
class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Room.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class ApplianceCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ApplianceCategorySerializer
    permission_classes = [IsSuperUserOrReadOnly]
    def get_queryset(self):
        return ApplianceCategory.objects.all()
class ApplianceViewSet(viewsets.ModelViewSet):
    serializer_class = ApplianceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appliance.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def set_status(self, request, pk=None):
        appliance = self.get_object()
        status = request.data.get('status')
        active_for = request.data.get('active_for') # in minutes

        if status not in ['active', 'inactive']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        appliance.status = status
        if status == 'active' and active_for:
            appliance.active_until = timezone.now() + datetime.timedelta(minutes=int(active_for))
        else:
            appliance.active_until = None

        appliance.save()
        return Response(self.get_serializer(appliance).data)

class AirConditionerViewSet(viewsets.ModelViewSet):
    serializer_class = AirConditionerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AirConditioner.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def set_temperature(self, request, pk=None):
        ac = self.get_object()
        temperature = request.data.get('temperature')

        if temperature is None:
            return Response({'error': 'Temperature not provided'}, status=status.HTTP_400_BAD_REQUEST)

        ac.temperature = float(temperature)
        ac.save()
        return Response(self.get_serializer(ac).data)
