# catalog/urls.py
from django.urls import path

from . import views

urlpatterns = [
    # Если пришёл запрос к относительному URL catalog/,
    # то запрос из корневого urls.py перенаправляется сюда, 
    # в файл catalog/urls.py;
    # и если в запросе после 'catalog/' ничего нет (пустая строка),
    # будет вызвана view-функция product_list() из файла catalog/views.py
    path('', views.product_list),

    # Если в запросе после 'catalog/' стоит '1/' или '2/',
    # будет вызвана view-функция product_detail() из файла catalog/views.py
    path('1/', views.product_detail),
    path('2/', views.product_detail),
]