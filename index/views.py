from django.shortcuts import render, redirect
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import Equipment
from .forms import EquipmentForm


def index(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EquipmentForm()

    # Получаем базовый список из PostgreSQL
    equipments_queryset = Equipment.objects.all().order_by('-id')
    current_date = timezone.now().date()

    # Создаем новый динамический список, где посчитаем всё на Python
    processed_equipments = []

    for item in equipments_queryset:
        # ВЫЧИСЛЯЕМ: Дата покупки + Срок гарантии в месяцах
        end_warranty_date = item.purchase_date + relativedelta(months=item.warranty_months)

        # СРАВНИВАЕМ: Если текущая дата строго больше даты окончания — гарантия истекла
        is_expired = current_date > end_warranty_date

        # Добавляем новые расчетные поля прямо в объект, чтобы прочитать их в HTML
        item.end_warranty_date = end_warranty_date
        item.is_expired = is_expired

        processed_equipments.append(item)

    # ЛОГИКА ФИЛЬТРАЦИИ И ПОИСКА (по нашему динамическому списку)
    search_query = request.GET.get('search', '')
    warranty_filter = request.GET.get('warranty', '')

    if search_query:
        # Ищем совпадения по серийному номеру (serial_number) вместо названия
        processed_equipments = [i for i in processed_equipments if search_query.lower() in i.serial_number.lower()]

    if warranty_filter == 'active':
        processed_equipments = [i for i in processed_equipments if not i.is_expired]
    elif warranty_filter == 'expired':
        processed_equipments = [i for i in processed_equipments if i.is_expired]

    context = {
        'username': 'Алексей',
        'form': form,
        'equipments': processed_equipments,  # Отдаем список с посчитанными датами
        'search_query': search_query,
        'warranty_filter': warranty_filter
    }
    return render(request, 'index.html', context)


def delete_equipment(request, item_id):
    item = Equipment.objects.get(id=item_id)
    item.delete()
    return redirect('index')
