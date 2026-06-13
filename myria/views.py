from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Car  


def home(request):
    cars = Car.objects.all()
    return render(request, 'main/home.html', {'cars': cars})

def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'main/cars_list.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'main/car_detail.html', {'car': car})


# 1. Функція для сторінки входу
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile_view')  # Перенаправляємо в кабінет після входу
    return render(request, 'main/login.html')

# 2. Функція для сторінки реєстрації
def register_view(request):
    if request.method == 'POST':
        # Використовуємо стандартну або твою кастомну логіку реєстрації
        # Для простоти — базова обробка:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Тут можна додати створення користувача:
        # User.objects.create_user(username=username, email=email, password=password)
        return redirect('login_view')
    return render(request, 'main/register.html')

# 3. Функція для особистого кабінету (доступна тільки авторизованим)
@login_required(login_url='login_view')
def profile_view(request):
    return render(request, 'main/profile.html')

# 4. Функція для виходу з акаунту
def logout_view(request):
    logout(request)
    return redirect('home')