from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('activate/<uid64>/<token>/', views.activate, name='activate'),
    path('reset_password/<uid64>/<token>/', views.resetPassword, name='reset_password'),
    path('new_password/', views.newPassword, name='new_password'),
    path('forget_password/', views.forgertPassword, name='forget_password'),
    
    path('user_profile/', views.userProfilePage, name="user_profile"),
    path('edit_user/', views.editUserPage, name="edit_user"),
    path('user/<str:user_slug>', views.userPage, name="user"),
    path('user/<str:user_slug>/<str:category_slug>/', views.userPage, name="recipe_category_user"),
]
