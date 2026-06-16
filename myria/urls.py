"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home, cars_list, car_detail, login_view, register_view, profile_view, logout_view, admin_panel_view
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('', home, name='home'),
    path('cars/', cars_list, name='car_list'),
    path('cars/<int:car_id>/', car_detail, name='car_detail'),
    path('login/', login_view, name='login_view'),            
    path('register/', register_view, name='register_view'),   
    path('profile/', profile_view, name='profile_view'), 
    path('admin_panel/', admin_panel_view, name='admin_panel_view'),      
    path('logout/', logout_view, name='logout_view'),

    path('api/me/', views.me, name='me'),
    path('api/admin-data/', views.admin_data, name='admin_data'),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
