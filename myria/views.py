from django.shortcuts import render, get_object_or_404
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