# homepage/urls.py

# Импортируем функцию path() 
# и файл homepage/views.py, в котором объявлена view-функция index().
from django.urls import path

from . import views

urlpatterns = [
    # Если вызван URL без относительного адреса (шаблон — пустые кавычки),
    # то вызывается view-функция index() из файла views.py
    path('', views.index),
]