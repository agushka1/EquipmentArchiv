from django.contrib import admin
from django.urls import path
from index import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('delete/<int:item_id>/', views.delete_equipment, name='delete_equipment'),
    # Новый маршрут для скачивания отчета
    path('download-report/', views.download_report, name='download_report'),
]
