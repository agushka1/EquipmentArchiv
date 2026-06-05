from django.shortcuts import render, redirect
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import Equipment
from .forms import EquipmentForm
from django.http import HttpResponse

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


def download_report(request):
    # 1. Забираем данные из БД
    equipments_queryset = Equipment.objects.all().order_by('name')
    current_date = timezone.now().date()

    active_warranty = []
    expired_warranty = []

    # 2. Сортируем устройства по статусу гарантии
    for item in equipments_queryset:
        end_warranty_date = item.purchase_date + relativedelta(months=item.warranty_months)
        item_info = f"• {item.name} | S/N: {item.serial_number} | Чек: {item.receipt_location} | Окончание гарантии: {end_warranty_date.strftime('%d.%m.%Y')}"

        if current_date > end_warranty_date:
            expired_warranty.append(item_info)
        else:
            active_warranty.append(item_info)

    # 3. Формируем текст самого файла
    report_text = "=== ОТЧЕТ ПО СОСТОЯНИЮ ОБОРУДОВАНИЯ СТРАНИЦЫ ===\n\n"

    report_text += f"🟢 НА ГАРАНТИИ (Всего: {len(active_warranty)})\n"
    report_text += "--------------------------------------------------\n"
    if active_warranty:
        report_text += "\n".join(active_warranty) + "\n"
    else:
        report_text += "Устройств на гарантии нет.\n"

    report_text += f"\n🔴 ГАРАНТИЯ ИСТЕКЛА (Всего: {len(expired_warranty)})\n"
    report_text += "--------------------------------------------------\n"
    if expired_warranty:
        report_text += "\n".join(expired_warranty) + "\n"
    else:
        report_text += "Устройств с истекшей гарантией нет.\n"

    # 4. Настраиваем HttpResponse так, чтобы браузер понял, что это файл для скачивания
    response = HttpResponse(report_text, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="equipment_report.txt"'

    return response