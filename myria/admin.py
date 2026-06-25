from django.contrib import admin
from .models import Car, CarImage, Brand, CarModel

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

# admin.site.register(Car)
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'year', 'price', 'mileage', 'city')
    inlines = [CarImageInline]

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'transport_type') 
    list_filter = ('transport_type',)       

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    list_filter = ('brand__transport_type', 'brand')
# Register your models here.
