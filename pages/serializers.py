from django.contrib.auth import authenticate

from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password



class PeripheralSerializer(serializers.ModelSerializer):
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=10)
    neededPins = models.IntegerField()
    icon = models.CharField(max_length=32)
    class Meta:
        model = Peripheral
        fields = ('name', 'type', 'neededPins', 'icon')

class MicrocontrollerSerializer(serializers.ModelSerializer):
    name = models.CharField(max_length=32)
    infoLink = models.URLField()
    availablePins = models.IntegerField()
    class Meta:
        model = Microcontroller
        fields = ('name', 'infoLink', 'availablePins')

class DeviceSerializer(serializers.ModelSerializer):
    microcontroller = models.ForeignKey(Microcontroller, on_delete=models.CASCADE)
    peripherals = models.ManyToManyField(Peripheral)
    class Meta:
        model = Device
        fields = ('microcontroller', 'peripherals')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8)
    devices = DeviceSerializer(many=True)
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'devices')
    def validate_password(self, value):
        return make_password(value)