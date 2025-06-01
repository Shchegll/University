from django.contrib import admin
from .models import Account, Relationship


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Настройки административного интерфейса для модели Account

    Определяет, как данные учетных записей будут отображаться и редактироваться
    в административной панели Django

    Attributes:
        display_items (tuple): Поля для отображения в списке записей
        filter_options (tuple): Поля, по которым можно фильтровать записи
        lookup_fields (tuple): Поля, по которым выполняется поиск
        missing_display (str): Замещающий текст для пустых значений
    """
    list_display = (
        'username',
        'pk',
        'email',
        'first_name',
        'last_name',
    )
    list_editable = ()
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    """Настройки административного интерфейса для модели Relationship

    Определяет отображение и редактирование связей между пользователями
    в административной панели Django

    Attributes:
        display_columns (tuple): Поля для отображения в списке связей
        editable_columns (tuple): Поля, доступные для редактирования в списке
        missing_value (str): Замещающий текст для пустых значений
    """
    list_display = ('pk', 'follower', 'target')
    list_editable = ()
    empty_value_display = '-пусто-'
