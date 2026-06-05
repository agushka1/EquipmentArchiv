from django.shortcuts import render, redirect
from .models import Equipment
from .forms import EquipmentForm

def index(request):
    # Если пользователь нажал кнопку на форме и отправил данные
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()  # Физически сохраняем новое оборудование в PostgreSQL
            return redirect('index')  # Перезагружаем страницу, чтобы очистить поля формы
    else:
        form = EquipmentForm()  # При обычном заходе создаем пустую форму

    # Забираем ВСЕ записи оборудования из базы данных
    equipments = Equipment.objects.all().order_by('-id')

    context = {
        'username': 'Алексей',
        'form': form,
        'equipments': equipments  # Передаем список техники в HTML
    }
    return render(request, 'index.html', context)
