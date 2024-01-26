from django.db import models
from django.contrib.auth.models import AbstractUser

class Microcontroller(models.Model):
    name = models.CharField(max_length=32)
    infoLink = models.URLField()
    availablePins = models.IntegerField()

    def __str__(self):
        return f"{self.id} | {self.name} - {self.availablePins}"
class Peripheral(models.Model):
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=10)
    neededPins = models.IntegerField()
    icon = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.id} | {self.name} - {self.type} - {self.neededPins}"


class DevicePeripheral(models.Model):
    peripheral = models.ForeignKey(Peripheral, on_delete=models.CASCADE)
    # device = models.ForeignKey(Device, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id} | {self.peripheral.name}"



class Device(models.Model):
    name = models.CharField(max_length=50, default = "Unnamed device")
    microcontroller = models.ForeignKey(Microcontroller, on_delete=models.CASCADE)
    peripherals = models.ManyToManyField(DevicePeripheral)
    def __str__(self):
        return f"{self.id} | {self.name} - {self.microcontroller.name}"



class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=128,blank=True)
    password = models.CharField(max_length=128)
    # from django.contrib.auth.hashers import make_password
    devices = models.ManyToManyField(Device)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']
    # REQUIRED_FIELDS = ['password']
    def __str__(self):
        return f"{self.email}"
class Read(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    peripheral = models.ForeignKey(DevicePeripheral, on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=32, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return f"{self.id} | {self.device.name} - {self.updated_at}"

class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    peripheral = models.ForeignKey(DevicePeripheral, on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=32, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return f"{self.id} | {self.device.name} - {self.updated_at}"