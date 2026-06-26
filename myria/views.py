from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from .models import Car, CarImage, CarModel, Brand
from django.http import JsonResponse
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
        first_name = (request.POST.get('username') or '').strip()
        last_name = (request.POST.get('last_name') or '').strip()
        phone_or_email = (request.POST.get('phone_or_email') or '').strip()
        password = request.POST.get('password') or ''

        errors = {}

        if not first_name:
            errors['username'] = "Введіть своє ім'я."

        if not phone_or_email:
            errors['phone_or_email'] = 'Введіть телефон або e-mail.'
        else:
            import re
            is_email = '@' in phone_or_email
            is_phone = re.fullmatch(r'[\+]?[\d\s\(\)\-]{7,15}', phone_or_email)

            if is_email:
                email_pattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$')
                if not email_pattern.match(phone_or_email):
                    errors['phone_or_email'] = 'Введіть коректний e-mail (наприклад, user@example.com).'
            elif not is_phone:
                errors['phone_or_email'] = 'Введіть коректний e-mail або номер телефону.'

        # Валідація пароля
        if not password or not password.strip():
            errors['password'] = 'Введіть пароль.'
        elif password != password.strip():
            errors['password'] = 'Пароль не може починатися або закінчуватися пробілами.'
        elif ' ' in password:
            errors['password'] = 'Пароль не може містити пробіли.'
        elif len(password) < 4:
            errors['password'] = 'Пароль повинен містити щонайменше 4 символів.'
        elif password.isdigit():
            errors['password'] = 'Пароль не може складатися лише з цифр.'

        # Перевірка унікальності
        if not errors and User.objects.filter(username=phone_or_email).exists():
            errors['phone_or_email'] = 'Користувач з таким телефоном або e-mail вже зареєстрований!'

        if errors:
            return render(request, 'main/register.html', {
                'errors': errors,
                'form_data': {
                    'username': first_name,
                    'last_name': last_name,
                    'phone_or_email': phone_or_email,
                }
            })

        user_email = phone_or_email if '@' in phone_or_email else ''

        user = User.objects.create_user(
            username=phone_or_email,
            email=user_email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        return redirect('login_view')

    return render(request, 'main/register.html')

def profile_view(request):
    return render(request, 'main/profile.html')

def admin_panel_view(request):
    return render(request, 'main/admin_panel.html')

# def add_car(request):
#     return render(request, 'main/add_car.html')

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


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """SessionAuthentication без CSRF-перевірки для GET-запитів через JS."""
    def enforce_csrf(self, request):
        return  


@api_view(['GET'])
@authentication_classes([CsrfExemptSessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_cars(request):
    """Отримання оголошень поточного користувача"""
    cars = Car.objects.filter(seller=request.user).order_by('-id')
    cars_data = []
    for c in cars:
        cars_data.append({
            'id': c.id,
            'brand': c.brand,
            'model_name': c.model_name,
            'year': c.year,
            'price': str(c.price),
            'currency': c.currency,
            'region': c.region,
            'city': c.city,
            'mileage': c.mileage,
            'main_photo': str(c.main_photo) if c.main_photo else None,
            'transport_type': c.transport_type,
        })
    return Response(cars_data)


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
        print("FILES:", request.FILES)  # ← додай це
        print("gallery_images:", request.FILES.getlist('gallery_images'))
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


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    """Получение списка всех пользователей"""
    users = User.objects.all().order_by('id')
    users_data = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_staff": u.is_staff
        } for u in users
    ]
    return Response(users_data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    """Удаление пользователя"""
    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            return Response({"error": "Не можна видалити головного суперюзера!"}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({"message": "Користувача успішно видалено"})
    except User.DoesNotExist:
        return Response({"error": "Користувача не знайдено"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_cars(request):
    """Отримання списку всіх оголошень (зв'язок через seller)"""
    try:
        cars = Car.objects.all().order_by('-id')
        cars_data = []
        
        for c in cars:
            if c.seller:
                author = c.seller.username
            else:
                author = "Не вказано"

            cars_data.append({
                "id": c.id,
                "brand": getattr(c, 'brand', '—'),
                "model_name": getattr(c, 'model_name', None) or getattr(c, 'model', '—'),
                "year": getattr(c, 'year', '—'),
                "transport_type": getattr(c, 'transport_type', '—'),
                "user": author  
            })
            
        return Response(cars_data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_car(request, car_id):
    """Удаление объявления администратором"""
    try:
        car = Car.objects.get(id=car_id)
        car.delete()
        return Response({"message": "Оголошення успішно видалено"})
    except Car.DoesNotExist:
        return Response({"error": "Оголошення не знайдено"}, status=status.HTTP_404_NOT_FOUND)
    
def load_brands(request):
    transport_type = request.GET.get('transport_type')
    brands = Brand.objects.filter(transport_type=transport_type).order_by('name')
    return JsonResponse(list(brands.values('id', 'name')), safe=False)

def load_models(request):
    brand_id = request.GET.get('brand_id')
    models = CarModel.objects.filter(brand_id=brand_id).order_by('name')
    return JsonResponse(list(models.values('id', 'name')), safe=False)