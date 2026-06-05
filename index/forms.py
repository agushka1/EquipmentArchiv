from django import forms
from .models import Equipment


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        # Добавили 'receipt_location' в список полей
        fields = ['name', 'serial_number', 'purchase_date', 'warranty_months', 'receipt_location']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Ноутбук Asus'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: SN123456789'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'warranty_months': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Например: 12'}),
            # Настройка внешнего вида для нового поля
            'receipt_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Б-2'}),
        }
