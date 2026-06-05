from django.contrib import admin
from django.urls import path
from index import views as index_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_views.index, name='index'),  # Указываем путь через точку
]
