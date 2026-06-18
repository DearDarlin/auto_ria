from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Car, CarImage  
from .forms import CarForm
import requests

def home(request):
    cars = Car.objects.all()
    return render(request, 'main/home.html', {'cars': cars})

def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'main/cars_list.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'main/car_detail.html', {'car': car})

def login_view(request):
    return render(request, 'main/login.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('username')  
        last_name = request.POST.get('last_name')
        phone_or_email = request.POST.get('phone_or_email').strip()  
        password = request.POST.get('password')
        system_username = phone_or_email 
        
        if User.objects.filter(username=system_username).exists():
            return render(request, 'main/register.html', {
                'error': 'Користувач з таким телефоном або e-mail вже зареєстрований!'
            })
            
        user_email = ""
        if "@" in phone_or_email:
            user_email = phone_or_email  

        user = User.objects.create_user(
            username=system_username,  
            email=user_email,
            password=password,
            first_name=first_name,   
            last_name=last_name        
        )
        return redirect('login_view')
            
    return render(request, 'main/register.html')

def profile_view(request):
    return render(request, 'main/profile.html')

def admin_panel_view(request):
    return render(request, 'main/admin_panel.html')

def add_car(request):
    return render(request, 'main/add_car.html')

def logout_view(request):
    logout(request)
    return redirect('home')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['username'] = self.user.username
        data['is_staff'] = self.user.is_staff
        data['is_superuser'] = self.user.is_superuser

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_data(request):
    return Response({
        'message': 'Ты админ. Доступ разрешён.',
        'secret': 'Это данные только для администратора.'
    })

def upload_to_imgbb(file_object):
    API_KEY = 'c1b8fa1435c084c7346d97362362be2d' 
    url = "https://api.imgbb.com/1/upload"
    
    files = {'image': (file_object.name, file_object, file_object.content_type)}
    payload = {'key': API_KEY}
    
    try:
        response = requests.post(url, data=payload, files=files)
        if response.status_code == 200:
            return response.json()['data']['url']
        else:
            print(f"Помилка завантаження: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Помилка завантаження: {e}")
    return None


def add_car_view(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            
            if request.user.is_authenticated:
                car.seller = request.user
            
            if 'main_photo' in request.FILES:
                main_url = upload_to_imgbb(request.FILES['main_photo'])
                if main_url:
                    car.main_photo = main_url
            
            car.save()
            
            gallery_files = request.FILES.getlist('gallery_images')
            for file in gallery_files:
                img_url = upload_to_imgbb(file)
                if img_url:
                    CarImage.objects.create(car=car, image=img_url)
                    
            return redirect('car_list') 
    else:
        form = CarForm()
        
    return render(request, 'main/add_car.html', {'form': form})