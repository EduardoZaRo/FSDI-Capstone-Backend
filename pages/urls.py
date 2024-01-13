from django.urls import path
from pages import views

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
    path('generate-code/', views.GenerateCode.as_view(), name="generate-code"),
]