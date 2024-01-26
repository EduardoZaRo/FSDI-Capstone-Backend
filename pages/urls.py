from django.urls import path
from pages import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # User auth URLS
    path('', views.ApiOverview.as_view()),
    path('login/', views.LoginView.as_view()),
    path('register/', views.SignupView.as_view()),
    path('is-authenticated/', views.CheckAuthenticatedView.as_view()),
    path('change-password/', views.ChangePassword.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('csrf-cookie/', views.GetCSRFToken.as_view()),
    path('all-users/', views.GetAllUsers.as_view()),

    #Devices funtionalities
    path('get-microcontrollers/', views.GetAllMicrocontrollers.as_view()),
    path('get-peripherals/', views.GetAllPeripherals.as_view()),
    path('get-devices/', views.GetAllDevices.as_view()),
    path('generate-code/', views.GenerateCode.as_view()),
    path('save-device/', views.SaveDevice.as_view()),
    path('get-user-devices/', views.GetUserDevices.as_view()),
    path('delete-device/', views.DeleteDevice.as_view()),
    path('get-device-read/', views.GetDeviceRead.as_view()),
    path('set-device-action/', views.SetDeviceAction.as_view()),
    # Microcontrollers endpoints
    path('save-from-microcontroller/', views.SaveFromMicrocontroller().as_view()),
    path('get-action-microcontroller/', views.GetActionMicrocontroller().as_view()),
]