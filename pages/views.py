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
            "delete-device": "https://eduardozaro.pythonanywhere.com/delete-device/",
            "get-device-read": "https://eduardozaro.pythonanywhere.com/get-device-read/",
            "----": "-----",
            "save-from-microcontroller": "https://eduardozaro.pythonanywhere.com/save-from-microcontroller/",
            "get-action-microcontroller": "https://eduardozaro.pythonanywhere.com/get-action-microcontroller/",

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
        name = device['name']
        microcontroller = device['microcontroller']
        peripherals = device['peripherals']
        codeTemplateByMicrocontroller = ""
        if(microcontroller['name'] == 'ESP32'):
            codeTemplateByMicrocontroller = 'code/esp32.html'
        elif(microcontroller['name'] == 'Arduino Uno R4'):
            codeTemplateByMicrocontroller = 'code/arduinoUnoR4.html'
        if(microcontroller['name'] == 'Raspberry Pi Pico'):
            codeTemplateByMicrocontroller = 'code/raspberryPiPico.html'
        htmlTextCode = render_to_string(codeTemplateByMicrocontroller, context={"name": name, "microcontroller": microcontroller, "peripherals": peripherals})


        response = Response(data = json.dumps({"code": htmlTextCode}), status = status.HTTP_200_OK)
        return response

class SaveDevice(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        device = request.data
        deviceName = device['name']
        microcontroller = device['microcontroller']
        peripherals = device['peripherals']
        microcontrollerObj = Microcontroller.objects.get(name=microcontroller['name'])


        # peripheralsObj = Peripheral.objects.filter(name__in=(p['title'] for p in peripherals))
        # deviceObj = Device.objects.create(name = deviceName,microcontroller=microcontrollerObj)
        # deviceObj.peripherals.add(*peripheralsObj)
        # request.user.devices.add(deviceObj)
        deviceperipheral_relation_list = []
        for peripheral in peripherals:
            peripheralObj = Peripheral.objects.get(name=peripheral['title'])
            devicePeripheralRelationObj = DevicePeripheral.objects.create(peripheral=peripheralObj)
            deviceperipheral_relation_list.append(devicePeripheralRelationObj)
        deviceObj = Device.objects.create(name = deviceName,microcontroller=microcontrollerObj)
        deviceObj.peripherals.add(*deviceperipheral_relation_list)
        request.user.devices.add(deviceObj)
        request.user.save()
        return Response(status = status.HTTP_200_OK)

class GetUserDevices(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        userObj = User.objects.get(email=self.request.user)
        user_serializer = serializers.UserSerializer(userObj).data
        return Response(data=user_serializer['devices'], status = status.HTTP_200_OK)

class DeleteDevice(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        Device.objects.get(id=request.data['id']).delete()
        return Response(status = status.HTTP_200_OK)

class GetDeviceRead(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # {
    #     "deviceID": 21,
    #     "peripheralID": 4
    # }
    def post(self, request):
        userObj = User.objects.get(email=self.request.user)
        deviceObj = Device.objects.get(id=request.data['deviceID'])
        peripheralObj = DevicePeripheral.objects.get(id=request.data['peripheralID'])
        readObj = Read.objects.get(user=userObj, device=deviceObj, peripheral=peripheralObj)
        read_serializer = serializers.ReadSerializer(readObj).data
        return Response(data = read_serializer, status = status.HTTP_200_OK)

class SetDeviceAction(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # {
    #     "device-id": 21,
    #     "peripheral-id": 4
    #     "value": 1
    # }
    def post(self, request):
        userObj = User.objects.get(email=self.request.user)
        deviceObj = Device.objects.get(id=request.data['deviceID'])
        peripheralObj = DevicePeripheral.objects.get(id=request.data['peripheralID'])
        Action.objects.filter(user=userObj, device=deviceObj, peripheral=peripheralObj).update(value=self.request.data["value"])
        return Response(data = {"xd", self.request.data["value"]}, status = status.HTTP_200_OK)


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
#     "name": "Incredible device",
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

class GetActionMicrocontroller(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        actionID = request.data['actionID']
        actionObj = Action.objects.get(id=actionID)
        action_serializer = serializers.ActionSerializer(actionObj).data
        return Response(data = {"value": action_serializer['value']}, status = status.HTTP_200_OK)

class SaveFromMicrocontroller(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        readID = request.data['readID']
        value = request.data['value']
        Read.objects.filter(id=readID).update(value=value)


        return Response(data = {"XDD": "XD"}, status = status.HTTP_200_OK)


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