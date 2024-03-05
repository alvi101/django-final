from django.urls import path
from .views import UserRegistrationView, UserLogin, ProfileView, Home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),

    # https://stackoverflow.com/questions/77690729/django-built-in-logout-view-method-not-allowed-get-users-logout
    path('logout/', LogoutView.as_view(), name='logout'),
]
