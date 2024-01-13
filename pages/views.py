from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
import json
from .models import *
from rest_framework import permissions
from rest_framework import views, status
from rest_framework.response import Response
from django.views import generic
from rest_framework import generics, status
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from rest_framework.decorators import api_view
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import socket
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from . import serializers
# https://docs.hektorprofe.net/django/api-django-rest/sistema-autenticacion-registro/
# send_mail('Subject here', 'Here is the message.', 'irvin.zavala@uabc.edu.mx', ['irvin.zavala@uabc.edu.mx'], fail_silently=False)

class ApiOverview(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        api_urls = {
            "login": "https://eduardozaro.pythonanywhere.com/login/",
            "register": "https://eduardozaro.pythonanywhere.com/register/",
            "profile": "https://eduardozaro.pythonanywhere.com/profile/",
            "is-authenticated": "https://eduardozaro.pythonanywhere.com/is-authenticated/ ",
            "change-password": "https://eduardozaro.pythonanywhere.com/change-password/ ",
            "reset-password": "https://eduardozaro.pythonanywhere.com/reset-password/ ",
            "csrf-cookie": "https://eduardozaro.pythonanywhere.com/csrf-cookie/",
            "all users": "https://eduardozaro.pythonanywhere.com/all-users/",
            "logout": "https://eduardozaro.pythonanywhere.com/logout/",
            "----": "-----",
            "get-microcontrollers": "https://eduardozaro.pythonanywhere.com/get-microcontrollers/",
            "get-peripherals": "https://eduardozaro.pythonanywhere.com/get-peripherals/",
            "get-devices": "https://eduardozaro.pythonanywhere.com/get-devices/",
            "generate-code": "https://eduardozaro.pythonanywhere.com/generate-code/",
            "save-device": "https://eduardozaro.pythonanywhere.com/save-device/",
            "get-user-devices": "https://eduardozaro.pythonanywhere.com/get-user-devices/",

        }
        return Response(api_urls)

class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)
        print(email, password)
        if user:
            login(request, user)
            print(serializers.UserSerializer(self.request.user).data)
            return Response(
                        serializers.UserSerializer(user).data,
                        status=status.HTTP_200_OK)
        return Response(status = status.HTTP_404_NOT_FOUND)
    def get_view_name(self):
        return "Mi login aca bien maniacote"

# @method_decorator(csrf_exempt, name='dispatch')
class LogoutView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        try:
            loggedInUser = serializers.UserSerializer(request.user).data
            return Response(loggedInUser)
        except:
            return Response("No logged in user")
    def post(self, request):
        logout(request)
        return Response(status = status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class SignupView(generics.CreateAPIView):
    '''
        SingupView handles the user registration inheriting CreatingAPIView
    '''
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer

class ProfileView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer
    def get_object(self):
        return self.request.user

@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        isAuthenticated = User.is_authenticated
        print(self.request.user.is_anonymous)
        # if isAuthenticated:
        if self.request.user.is_authenticated:
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_404_NOT_FOUND)




@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        return Response(data = {'X-CSRFToken': get_token(request)},status = status.HTTP_200_OK)


class GetAllUsers(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        users = User.objects.all()
        serializer_data = serializers.UserSerializer(users, many=True).data
        return Response(data = serializer_data,status = status.HTTP_200_OK)







class ChangePassword(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class GetAllPeripherals(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        peripherals = Peripheral.objects.all()
        serializer_data = serializers.PeripheralSerializer(peripherals, many=True).data
        return Response(data = serializer_data,status = status.HTTP_200_OK)

class GetAllMicrocontrollers(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        microcontrollers = Microcontroller.objects.all()
        serializer_data = serializers.MicrocontrollerSerializer(microcontrollers, many=True).data
        return Response(data = serializer_data,status = status.HTTP_200_OK)

class GetAllDevices(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        device = Device.objects.all()
        serializer_data = serializers.DeviceSerializer(device, many=True).data
        return Response(data = serializer_data,status = status.HTTP_200_OK)

class GenerateCode(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        device = request.data
        microcontroller = device['microcontroller']
        peripherals = device['peripherals']
        htmlTextCode = render_to_string('code/base.html', context={"peripherals":peripherals})
        response = Response(data = json.dumps({"code": htmlTextCode}), status = status.HTTP_200_OK)
        response["Access-Control-Allow-Origin"] = "*"
        # print("microcontroller",microcontroller)
        # microcontrollerObj = Microcontroller.objects.get(name=microcontroller['name'])
        # peripheralsObj = Peripheral.objects.filter(name__in=(p['title'] for p in peripherals))
        # deviceObj = Device.objects.create(microcontroller=microcontrollerObj)
        # deviceObj.peripherals.add(*peripheralsObj)
        # for peripheral in peripherals:
        #     devicesObj.peripherals.add(peripheral
        return response

class SaveDevice(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        device = request.data
        microcontroller = device['microcontroller']
        peripherals = device['peripherals']
        microcontrollerObj = Microcontroller.objects.get(name=microcontroller['name'])
        peripheralsObj = Peripheral.objects.filter(name__in=(p['title'] for p in peripherals))
        deviceObj = Device.objects.create(microcontroller=microcontrollerObj)
        deviceObj.peripherals.add(*peripheralsObj)
        request.user.devices.add(deviceObj)
        request.user.save()
        return Response(status = status.HTTP_200_OK)

class GetUserDevices(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        userObj = User.objects.get(email=self.request.user)
        user_serializer = serializers.UserSerializer(userObj).data
        return Response(data=user_serializer['devices'], status = status.HTTP_200_OK)
        # userObj = User.objects.filter(email=self.request.user)
        # user_serializer = serializers.UserSerializer(data=userObj)
        # print(userObj, user_serializer)
        # if user_serializer.is_valid():
        #     return Response(data=user_serializer.data, status = status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        # serializer = serializers.UserSerializer(data=request.user)
        # if serializer.is_valid():
        #     serializer_data = User.objects.filter(email=serializer.data.get('email')).data
        #     return Response(data = serializer_data,  status = status.HTTP_200_OK)
        # return Response(status = status.HTTP_400_BAD_REQUEST)

# class ChangePassword(views.APIView):
#     permission_classes = (permissions.AllowAny,)
#     def post(self, request):
#         serializer = serializers.ChangePasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             if user.check_password(serializer.data.get('old_password')):
#                 user.set_password(serializer.data.get('new_password'))
#                 user.save()
#                 update_session_auth_hash(request, user)  # To update session after password change
#                 return Response(status=status.HTTP_200_OK)
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

# Sample device
# {
#     "microcontroller": {
#         "name": "ESP32",
#         "availablePins": 32,
#         "infoLink": "https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf",
#         "_id": "1"
#     },
#     "peripherals": [{
#         "title": "LED",
#         "type": "INPUT",
#         "position": "left",
#         "icon": "lightbulb",
#         "neededPins": 1,
#         "_id": "1"
#     }]
# }


@csrf_exempt
def home(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        requeson = json.loads(body_unicode) #request + json
        if(requeson["LED_STATE"] == 0):
            return HttpResponse(json.dumps({"ACTIVATE_LED": 1}))
        return HttpResponse(json.dumps({"ACTIVATE_LED": 0}))
    return render(request, 'pages/home.html')




@csrf_exempt
def save_led_state(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        requeson = json.loads(body_unicode) #request + json
        row = LED.objects.create(state=requeson["LED_STATE"])
        row.save()
        return HttpResponse("OK")
    return HttpResponse("OK")

@csrf_exempt
def get_led_state(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        requeson = json.loads(body_unicode) #request + json
        lastState = LED.objects.all().last()

        response = HttpResponse(json.dumps({"LED_STATE": 1 if lastState.state == True else 0}))
        response["Access-Control-Allow-Origin"] = "*"

        return response
    return HttpResponse("OK")