from rest_framework import serializers
from .models import Appliance, ApplianceCategory, Room, AirConditioner

class RoomSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Room
        fields = '__all__'

class ApplianceCategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = ApplianceCategory
        fields = '__all__'

class ApplianceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Appliance
        fields = '__all__'

class AirConditionerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = AirConditioner
        fields = '__all__'
