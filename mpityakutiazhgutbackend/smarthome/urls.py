from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ApplianceCategoryViewSet, ApplianceViewSet, AirConditionerViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'appliance-categories', ApplianceCategoryViewSet, basename='appliancecategory')
router.register(r'appliances', ApplianceViewSet, basename='appliance')
router.register(r'air-conditioners', AirConditionerViewSet, basename='airconditioner')

urlpatterns = [
    path('', include(router.urls)),
]
