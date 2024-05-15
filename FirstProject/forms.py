from django import forms
from django.contrib.auth.forms import UserCreationForm

from FirstProject.models import Housing
from django.core.exceptions import ValidationError


class HousingForm(forms.Form):
    area = forms.IntegerField(min_value=10, max_value=1900, help_text="Введите площадь жилья (м²)")
    address = forms.CharField(max_length=100, help_text="Укажите адрес жилья")
    cost = forms.IntegerField(min_value=10, max_value=100000000000, help_text="Введите стоимость жилья")


class residentForm(forms.Form):
    first_name = forms.CharField(help_text="Введите имя")
    last_name = forms.CharField(help_text="Введите фамилию")
    district = forms.CharField(help_text="Выберите дату рождения")
"""    photo = forms.ImageField(help_text="Введите номер команды")
"""