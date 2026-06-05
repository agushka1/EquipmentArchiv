from django.contrib import admin
from django.urls import path
from index import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # Django ищет именно это имя: name='delete_equipment'
    path('delete/<int:item_id>/', views.delete_equipment, name='delete_equipment'),
]
