from django.contrib import admin
from .models import Equipment  # Импортируем только оборудование

admin.site.register(Equipment)
