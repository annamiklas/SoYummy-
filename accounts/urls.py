from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('activate/<uid64>/<token>/', views.activate, name='activate'),
    path('reset_password/<uid64>/<token>/', views.reset_password, name='reset_password'),
    path('new_password/', views.new_password, name='new_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    
    path('user_profile/', views.user_profile_page, name="user_profile"),
    path('edit_user/', views.edit_user_page, name="edit_user"),
    path('user/<str:user_slug>', views.user_page, name="user"),
    path('user/<str:user_slug>/<str:category_slug>/', views.user_page, name="recipe_category_user"),
]
