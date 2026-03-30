from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name

class ApplianceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Appliance(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ApplianceCategory, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    active_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class AirConditioner(Appliance):
    temperature = models.FloatField(default=22.0)

    def __str__(self):
        return f"{self.name} (AC)"
