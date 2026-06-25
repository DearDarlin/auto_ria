from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


TRANSPORT_CHOICES = [
        ('Легкові', 'Легкові'), ('Мото', 'Мото'), ('Вантажівки', 'Вантажівки'),
        ('Причепи', 'Причепи'), ('Спецтехніка', 'Спецтехніка'), 
        ('Сільгосптехніка', 'Сільгосптехніка'), ('Автобуси', 'Автобуси'),
        ('Водний транспорт', 'Водний транспорт'), ('Повітряний транспорт', 'Повітряний транспорт'),
        ('Автобудинки', 'Автобудинки'),
    ]

def current_year():
    return datetime.date.today().year

class Brand(models.Model):
    transport_type = models.CharField(max_length=50, choices=TRANSPORT_CHOICES, verbose_name="Тип транспорту")
    name = models.CharField(max_length=100, verbose_name="Марка авто")

    def __str__(self):
        return f"{self.name} {self.transport_type}"
    
class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models', verbose_name="Тип транспорту")
    name = models.CharField(max_length=100, verbose_name="Модель")

    def __str__(self):
        return self.name

class Car(models.Model):

    

    REGION_CHOICES = [
        ('Київ', 'Київ'), ('Вінниця', 'Вінниця'), ('Кропивницький', 'Кропивницький (Кіровоград)'),
        ('Полтава', 'Полтава'), ('Черкаси', 'Черкаси'), ('Тернопіль', 'Тернопіль'),
        ('Хмельницький', 'Хмельницький'), ('Львів', 'Львів'), ('Рівне', 'Рівне'),
        ('Івано-Франківськ', 'Івано-Франківськ'), ('Луцьк', 'Луцьк'), ('Ужгород', 'Ужгород'),
        ('Чернівці', 'Чернівці'), ('Харків', 'Харків'), ('Дніпро', 'Дніпро (Дніпропетровськ)'),
        ('Донецька обл.', 'Донецька обл.'), ('Запоріжжя', 'Запоріжжя'), ('Одеса', 'Одеса'),
        ('Миколаїв', 'Миколаїв'), ('Херсон', 'Херсон'), ('Житомир', 'Житомир'),
        ('Чернігів', 'Чернігів'), ('Суми', 'Суми'),
    ]

    COUNTRY_CHOICES = [
        ('Австралія', 'Австралія'), ('Австрія', 'Австрія'), ('Алжир', 'Алжир'), ('Англія', 'Англія'),
        ('Аргентина', 'Аргентина'), ('Бельгія', 'Бельгія'), ('Білорусь', 'Білорусь'), ('Болгарія', 'Болгарія'),
        ('Бразилія', 'Бразилія'), ('Греція', 'Греція'), ('Грузія', 'Грузія'), ('Данія', 'Данія'),
        ('Естонія', 'Естонія'), ('Єгипет', 'Єгипет'), ('Ізраїль', 'Ізраїль'), ('Індія', 'Індія'),
        ('Іран', 'Іран'), ('Ірландія', 'Ірландія'), ('Ісландія', 'Ісландія'), ('Іспанія', 'Іспанія'),
        ('Італія', 'Італія'), ('Казахстан', 'Казахстан'), ('Канада', 'Канада'), ('Китай', 'Китай'),
        ('Корея', 'Корея'), ('Латвія', 'Латвія'), ('Литва', 'Литва'), ('Люксембург', 'Люксембург'),
        ('Малайзія', 'Малайзія'), ('Молдова', 'Молдова'), ('Монако', 'Монако'), ('Нідерланди', 'Нідерланди'),
        ('Німеччина', 'Німеччина'), ('Норвегія', 'Норвегія'), ('ОАЕ', 'ОАЕ'), ('Польша', 'Польща'),
        ('Португалiя', 'Португалія'), ('Румунія', 'Румунія'), ('Сербія', 'Сербія'), ('Словаччина', 'Словаччина'),
        ('Словенія', 'Словенія'), ('США', 'США'), ('Таджикистан', 'Таджикистан'), ('Таїланд', 'Таїланд'),
        ('Тайвань', 'Тайвань'), ('Туреччина', 'Туреччина'), ('Угорщина', 'Угорщина'), ('Узбекистан', 'Узбекистан'),
        ('Фінляндія', 'Фінляндія'), ('Франція', 'Франція'), ('Хорватія', 'Хорватія'), ('Чехія', 'Чехія'),
        ('Швейцарія', 'Швейцарія'), ('Швеція', 'Швеція'), ('Японія', 'Японія'),
    ]

    ACCIDENT_CHOICES = [('Ні, не був у ДТП', 'Ні, не був у ДТП'), ('Так, був у ДТП', 'Так, був у ДТП')]
    CONDITIONER_CHOICES = [('Кондиціонер', 'Кондиціонер'), ('Клімат-контроль 1-зонний', 'Клімат-контроль 1-зонний'), ('Клімат-контроль 2-зонний', 'Клімат-контроль 2-зонний'), ('Клімат-контроль багатозонний', 'Клімат-контроль багатозонний')]
    WINDOWS_CHOICES = [('Передні', 'Передні'), ('Передні та задні', 'Передні та задні')]
    MATERIAL_CHOICES = [('Тканина', 'Тканина'), ('Шкіра', 'Шкіра'), ('Велюр', 'Велюр'), ('Комбінований', 'Комбінований'), ('Штучна шкіра', 'Штучна шкіра'), ('Алькантара', 'Алькантара')]
    INTERIOR_COLOR_CHOICES = [('Світлий', 'Світлий'), ('Темний', 'Темний'), ('Коричневий', 'Коричневий')]
    STEERING_ASSIST_CHOICES = [('Гідро', 'Гідро'), ('Електро', 'Електро')]
    STEERING_ADJ_CHOICES = [('По висоті', 'По висоті'), ('По висоті та по вильоту', 'По висоті та по вильоту')]
    SPARE_WHEEL_CHOICES = [('Повнорозмірне', 'Повнорозмірне'), ('Докатка', 'Докатка')]
    HEADLIGHTS_CHOICES = [('Ксенонові/Біксенонові', 'Ксенонові/Біксенонові'), ('Лазерні', 'Лазерні'), ('Світлодіодні', 'Світлодіодні'), ('Матричні', 'Матричні'), ('Галогенні', 'Галогенні')]
    SEAT_HEIGHT_CHOICES = [('Ручне регулювання сидіння водія', 'Ручне регулювання сидіння водія'), ('Ручне регулювання передніх сидінь', 'Ручне регулювання передніх сидінь'), ('Електрорегулювання сидіння водія', 'Електрорегулювання сидіння водія'), ('Електрорегулювання передніх сидінь', 'Електрорегулювання передніх сидінь'), ('Електрорегулювання передніх та задніх сидінь', 'Електрорегулювання передніх та задніх сидінь')]
    SEAT_MEMORY_CHOICES = [('Сидіння водія', 'Сидіння водія'), ('Передні сидіння', 'Передні сидіння'), ('Передні та задні сидіння', 'Передні та задні сидіння')]
    HEATING_VENT_CHOICES = [('Передні сидіння', 'Передні сидіння'), ('Передні та задні сидіння', 'Передні та задні сидіння')]
    CURRENCY_CHOICES = [('$', '$'), ('€', '€'), ('грн.', 'грн.')]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_cars', null=True, blank=True)
    
    main_photo = models.ImageField(upload_to='cars_photos/', blank=True, null=True, verbose_name="Головне фото")
    youtube_link = models.URLField(max_length=255, blank=True, null=True, verbose_name="Додати відео з YouTube")

    transport_type = models.CharField(max_length=50, choices=TRANSPORT_CHOICES, verbose_name="Тип транспорту")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, verbose_name="Марка авто")
    model_name = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True,max_length=100, verbose_name="Модель авто")
    
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(current_year)],
        verbose_name="Рік випуску"
    )
    mileage = models.IntegerField(verbose_name="Пробіг (тис. км)")
    body_type = models.CharField(max_length=100, verbose_name="Тип кузова", blank=True, null=True)
    modification = models.CharField(max_length=100, blank=True, null=True, verbose_name="Модифікація")
    
    region = models.CharField(max_length=50, choices=REGION_CHOICES, verbose_name="Регіон")
    city = models.CharField(max_length=100, verbose_name="Місто")
    vin_code = models.CharField(max_length=17, blank=True, null=True, verbose_name="VIN-код")
    is_owner = models.BooleanField(default=True, verbose_name="Ви власник авто?")


    description = models.TextField(max_length=2000, verbose_name="Опис автомобіля")

    color = models.CharField(max_length=50, verbose_name="Колір")
    imported_from = models.CharField(max_length=50, choices=COUNTRY_CHOICES, blank=True, null=True, verbose_name="Пригнаний з")
    accident = models.CharField(max_length=50, choices=ACCIDENT_CHOICES, blank=True, null=True, verbose_name="Участь в ДТП")
    paintwork = models.CharField(max_length=100, blank=True, null=True, verbose_name="Лакофарбове покриття")
    technical_state = models.CharField(max_length=100, blank=True, null=True, verbose_name="Технічний стан")

    conditioner = models.CharField(max_length=50, choices=CONDITIONER_CHOICES, blank=True, null=True, verbose_name="Кондиціонер")
    windows = models.CharField(max_length=50, choices=WINDOWS_CHOICES, blank=True, null=True, verbose_name="Електросклопідйомники")
    interior_material = models.CharField(max_length=50, choices=MATERIAL_CHOICES, blank=True, null=True, verbose_name="Матеріали салону")
    interior_color = models.CharField(max_length=50, choices=INTERIOR_COLOR_CHOICES, blank=True, null=True, verbose_name="Колір салону")
    steering_assist = models.CharField(max_length=50, choices=STEERING_ASSIST_CHOICES, blank=True, null=True, verbose_name="Підсилювач керма")
    steering_adjustment = models.CharField(max_length=50, choices=STEERING_ADJ_CHOICES, blank=True, null=True, verbose_name="Регулювання керма")
    spare_wheel = models.CharField(max_length=50, choices=SPARE_WHEEL_CHOICES, blank=True, null=True, verbose_name="Запасне колесо")
    headlights = models.CharField(max_length=50, choices=HEADLIGHTS_CHOICES, blank=True, null=True, verbose_name="Фари")
    seat_height = models.CharField(max_length=50, choices=SEAT_HEIGHT_CHOICES, blank=True, null=True, verbose_name="Регулювання сидінь по висоті")
    seat_memory = models.CharField(max_length=50, choices=SEAT_MEMORY_CHOICES, blank=True, null=True, verbose_name="Пам'ять положення сидіння")
    seat_heating = models.CharField(max_length=50, choices=HEATING_VENT_CHOICES, blank=True, null=True, verbose_name="Підігрів сидінь")
    seat_ventilation = models.CharField(max_length=50, choices=HEATING_VENT_CHOICES, blank=True, null=True, verbose_name="Вентиляція сидінь")


    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='$', verbose_name="Валюта")
    bargain_possible = models.BooleanField(default=False, verbose_name="Торг")
    exchange_possible = models.BooleanField(default=False, verbose_name="Обмін")

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.year})"
    
class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.URLField(max_length=500, verbose_name="Посилання на додаткове фото")

    class Meta:
        verbose_name = "Додаткове фото"
        verbose_name_plural = "Додаткові фото"

    def __str__(self):
        return f"Фото для {self.car.brand} {self.car.model_name}"