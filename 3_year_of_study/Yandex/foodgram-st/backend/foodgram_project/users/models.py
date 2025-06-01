from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    """Модель пользовательского аккаунта, расширяющая стандартную модель

    Добавляет дополнительное поле для контактного email
    Наследует все стандартные поля Django User

    Attributes:
        contact_email Уникальный email для контактов
    """
    contact_email = models.EmailField(max_length=250, unique=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Учетная запись'
        verbose_name_plural = 'Учетные записи'

    def __str__(self):
        return self.username


class Relationship(models.Model):
    """Модель для представления отношений подписки между пользователями.

    Создает связь "подписчик -> подписка" между двумя пользователями (Account)
    Гарантирует уникальность каждой пары подписчик-подписка через constraint

    Attributes:
        follower (ForeignKey): Пользователь, который подписывается (подписчик)
        target (ForeignKey): Пользователь, на которого подписываются
    """
    follower = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='initiated_connections',
        verbose_name='Последователь'
    )
    target = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='received_connections',
        verbose_name='Объект подписки'
    )

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'target'],
                name='connection_unique'
            )
        ]

    def __str__(self):
        return f'{self.follower} -> {self.target}'
