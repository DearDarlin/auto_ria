from django.contrib import admin
from .models import Car, CarImage

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

# admin.site.register(Car)
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price', 'mileage', 'fuel', 'city')
    inlines = [CarImageInline]
# Register your models here.
