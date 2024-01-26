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
        fields = ('id', 'name', 'type', 'neededPins', 'icon')

class MicrocontrollerSerializer(serializers.ModelSerializer):
    name = models.CharField(max_length=32)
    infoLink = models.URLField()
    availablePins = models.IntegerField()
    class Meta:
        model = Microcontroller
        fields = ('id', 'name', 'infoLink', 'availablePins')

class DevicePeripheralSerializer(serializers.ModelSerializer):
    peripheral = PeripheralSerializer()
    class Meta:
        model = DevicePeripheral
        fields = ('id', 'peripheral')

class DeviceSerializer(serializers.ModelSerializer):
    # microcontroller = models.ForeignKey(Microcontroller, on_delete=models.CASCADE)
    # peripherals = models.ManyToManyField(Peripheral)
    name = models.CharField(max_length=50, default = "Unnamed device")
    microcontroller = MicrocontrollerSerializer()
    peripherals = DevicePeripheralSerializer(many=True)
    class Meta:
        model = Device
        fields = ('id', 'name', 'microcontroller', 'peripherals')

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

class ReadSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    device = DeviceSerializer()
    peripheral = DevicePeripheralSerializer()
    value = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        model = Read
        fields = ('id', 'user', 'device', 'peripheral', 'value', 'created_at', 'updated_at')

class ActionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    device = DeviceSerializer()
    peripheral = DevicePeripheralSerializer()
    value = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        model = Read
        fields = ('id', 'user', 'device', 'peripheral', 'value', 'created_at', 'updated_at')