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
from .views import home, cars_list, car_detail, login_view, register_view, profile_view, logout_view, admin_panel_view, add_car_view
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
    path('add_car/', views.add_car_view, name='add_car'),

    path('api/me/', views.me, name='me'),
    path('api/my-cars/', views.my_cars, name='my_cars'),
    path('api/admin-data/', views.admin_data, name='admin_data'),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/admin/users/', views.get_all_users, name='admin_users_list'),
    path('api/admin/users/<int:user_id>/delete/', views.delete_user, name='admin_delete_user'),
    path('api/admin/cars/', views.get_all_cars, name='admin_cars_list'),
    path('api/admin/cars/<int:car_id>/delete/', views.delete_car, name='admin_delete_car'),

    path('ajax/load-brands/', views.load_brands, name='ajax_load_brands'),
    path('ajax/load-models/', views.load_models, name='ajax_load_models'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),

   path('search/', views.search_cars, name='search_cars'),

]