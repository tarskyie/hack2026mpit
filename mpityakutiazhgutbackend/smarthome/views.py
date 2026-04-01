from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Appliance, ApplianceCategory, Room, AirConditioner
from .serializers import ApplianceSerializer, ApplianceCategorySerializer, RoomSerializer, AirConditionerSerializer
from django.utils import timezone
import datetime
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperUserOrReadOnly

last_home_access = None

class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        global last_home_access
        last_home_access = timezone.now()

        rooms = Room.objects.filter(user=request.user)
        data = []
        for room in rooms:
            room_data = {
                'id': room.id,
                'name': room.name,
                'appliances': []
            }
            appliances = Appliance.objects.filter(room=room)
            for appliance in appliances:
                appliance_data = {
                    'id': appliance.id,
                    'name': appliance.name,
                    'status': appliance.status,
                    'category': appliance.category.name,
                    'active_until': appliance.active_until
                }
                if hasattr(appliance, 'airconditioner'):
                    appliance_data['temperature'] = appliance.airconditioner.temperature
                room_data['appliances'].append(appliance_data)
            data.append(room_data)
        return Response(data)

class HomeIsOnlineView(APIView):
    def get(self, request):
        global last_home_access
        if last_home_access and (timezone.now() - last_home_access) < datetime.timedelta(seconds=10):
            return Response("online")
        else:
            return Response("offline")

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Room.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_destroy(self, instance):
        instance.delete()

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
    
    def perform_destroy(self, instance):
        instance.delete()

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
