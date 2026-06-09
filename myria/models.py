from django.db import models

class Car(models.Model):
    brand = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Рік випуску")
    price = models.IntegerField(verbose_name="Ціна ($)")
    mileage = models.CharField(max_length=30, verbose_name="Пробіг")
    fuel = models.CharField(max_length=50, verbose_name="Тип пального / Двигун")
    city = models.CharField(max_length=50, verbose_name="Місто")
    image = models.URLField(max_length=300, blank=True, null=True, verbose_name="Посилання на фото")
    transmission = models.CharField(max_length=50, default="Ручна / Механіка", verbose_name="Коробка передач")
    color = models.CharField(max_length=50, default="Білий", verbose_name="Колір")
    car_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Державний номер")
    vin_code = models.CharField(max_length=30, blank=True, null=True, verbose_name="VIN-код")
    description = models.TextField(blank=True, null=True, verbose_name="Опис від власника")

    class Meta:
        verbose_name = "Автомобіль"
        verbose_name_plural = "Автомобілі"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.URLField(max_length=500, verbose_name="Посилання на додаткове фото")

    class Meta:
        verbose_name = "Додаткове photo"
        verbose_name_plural = "Додаткові фото"

    def __str__(self):
        return f"Фото для {self.car.brand} {self.car.model}"