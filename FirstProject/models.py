from django.db import models
from django.contrib.auth.models import User, AbstractUser


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value,  self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(**kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Countrie(models.Model):
    name = models.CharField(max_length=100, verbose_name="Страна",
                            help_text="Введите название страны", null=False, blank=True)
    capital = models.CharField(max_length=50, verbose_name="Столица",
                               help_text="Введите столицу этой страны", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Countrie"


class Government(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя", help_text="Введите имя", null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", help_text="Введите фамилию",
                                 null=True, blank=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id представителя власти",
                                help_text="Выберите id представителя", null=True, blank=True)
    photo = models.ImageField(blank=True, null=True, upload_to="images")
    country = models.ForeignKey(Countrie, on_delete=models.CASCADE, verbose_name="Страна",
                                help_text="Выберите страну представителя власти", null=True, blank=True)

    def __str__(self):
        return "Представитель власти: " + self.first_name + " " + self.last_name

    class Meta:
        db_table = "Government"


class District(models.Model):
    name = models.CharField(max_length=100, verbose_name="Район",
                            help_text="Введите район города", null=False, blank=True)
    population = IntegerRangeField(min_value=10, max_value=18000000, verbose_name="Численность населения района",
                             help_text="Введите численность района", null=True, blank=True)

    def __str__(self):
        return "Район: " + self.name

    class Meta:
        db_table = "District"


class Citie(models.Model):
    name_city = models.CharField(max_length=100, primary_key=True, verbose_name="Город",
                                 help_text="Введите название города", null=False, blank=True)
    country = models.ForeignKey(Countrie, on_delete=models.CASCADE, verbose_name="Страна",
                                help_text="Введите название страны, в которой находится этот город",
                                null=True, blank=True)
    government = models.ForeignKey(Government, on_delete=models.CASCADE, verbose_name="Власть",
                                   help_text="Выберите представителя власти",null=True, blank=True)
    districts = models.ManyToManyField(District)

    def __str__(self):
        return "Город: " + self.name_city

    class Meta:
        db_table = "Citie"


class Resident(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя", help_text="Введите имя", null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", help_text="Введите фамилию",
                                 null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Район города",
                                 help_text="Введите район города", null=True, blank=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE,  verbose_name="id жителя",
                                help_text="Выберите id жителя", null=True, blank=True)
    photo = models.ImageField(blank=True, null=True, upload_to="images")

    def __str__(self):
        return "Житель: " + self.first_name + " " + self.last_name

    class Meta:
        db_table = "Resident"


class Housing(models.Model):

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, verbose_name="Житель",
                                 help_text="Введите имя и фамилию жителя", null=True, blank=True)
    area = IntegerRangeField(min_value=10, max_value=18000000, verbose_name="Площадь",
                             help_text="Введите площадь жилья", null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name= "Адрес", help_text="Укажите адрес жилья", null=True, blank=True)
    cost = IntegerRangeField(min_value=10, max_value=180000000000, verbose_name="Стоимость",
                             help_text="Введите стоимость жилья",null=True, blank=True)
    city = models.ForeignKey(Citie, on_delete=models.CASCADE, verbose_name="Город",
                             help_text="Введите название города", null=True, blank=True)

    def __str__(self):
        return self.resident.__str__() + " проживает по адресу " + str(self.address)

    class Meta:
        db_table = "Housing"

