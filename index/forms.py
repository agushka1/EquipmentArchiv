from django import forms
from .models import Equipment


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        # Указываем все поля нашей новой таблицы
        fields = ['name', 'serial_number', 'purchase_date', 'warranty_months']

        # Настраиваем внешний вид и подсказки для полей
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Ноутбук Asus'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: SN123456789'}),
            # Важно: ставим тип 'date', чтобы в браузере открывался удобный календарь
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'warranty_months': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Например: 12'}),
        }
