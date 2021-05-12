from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('activate/<uid64>/<token>/', views.activate, name='activate'),
    
    path('user_profile/', views.userProfilePage, name="user_profile"),
    path('edit_user/', views.editUserPage, name="edit_user"),
    path('user/<str:idU>', views.userPage, name="user"),
]
