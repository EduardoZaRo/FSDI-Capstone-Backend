from django.db import models
from django.contrib.auth.models import AbstractUser
class Microcontroller(models.Model):
    name = models.CharField(max_length=32)
    infoLink = models.URLField()
    availablePins = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} - {self.availablePins}"
class Peripheral(models.Model):
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=10)
    neededPins = models.IntegerField()
    icon = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.name} - {self.type} - {self.neededPins}"
class Device(models.Model):
    microcontroller = models.ForeignKey(Microcontroller, on_delete=models.CASCADE)
    peripherals = models.ManyToManyField(Peripheral)
    def __str__(self):
        return f"{self.microcontroller.name}"
    
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
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.timestamp}"
    
class Action(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.timestamp}"