from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from users.models import Account


class Ingredient(models.Model):
    """Модель ингредиента для рецептов

    Attributes:
        name (CharField): Название ингредиента
        measurement_unit (CharField): Единица измерения ингредиента
    """
    name = models.CharField(
        'Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag_my(models.Model):
    """Модель тега для категоризации рецептов

    Attributes:
        name (CharField): Название тега
        color (CharField): HEX-код цвета тега
        slug (SlugField): Уникальный идентификатор тега
    """
    name = models.CharField(
        'Название тега',
        max_length=200
    )
    color = models.CharField(
        'HEX-код цвета',
        max_length=7,
        null=True,
        validators=[
            RegexValidator(
                regex='^#([a-fA-F0-9]{6})$',
                message='Значение должно быть в HEX-формате (#RRGGBB).'
            )
        ]
    )
    slug = models.SlugField(
        'Уникальный идентификатор',
        max_length=200,
        unique=True,
        null=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Основная модель рецепта

    Attributes:
        name (CharField): Название рецепта
        text (TextField): Текст рецепта (описание)
        cooking_time (PositiveIntegerField): Время приготовления в минутах
        image (ImageField): Изображение готового блюда
        pub_date (DateTimeField): Дата публикации рецепта
        author (ForeignKey): Автор рецепта (связь с моделью Account)
        tags (ManyToManyField): Теги, связанные с рецептом
    """
    name = models.CharField(
        'Название рецепта',
        max_length=200
    )
    text = models.TextField(
        'Текст рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления (минуты)',
        validators=[MinValueValidator(1)]
    )
    image = models.ImageField(
        'Изображение блюда',
        upload_to='recipes/',
        blank=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Recipe_ing',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag_my,
        verbose_name='Теги'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favor(models.Model):
    """Модель для хранения избранных рецептов пользователей

    Attributes:
        user (ForeignKey): Пользователь, добавивший рецепт в избранное
        recipe (ForeignKey): Рецепт, добавленный в избранное
    """
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorites',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class Recipe_ing(models.Model):
    """Промежуточная модель для связи рецептов и ингредиентов с указанием колво

    Attributes:
        recipe (ForeignKey): Связанный рецепт
        ingredient (ForeignKey): Связанный ингредиент
        amount (PositiveIntegerField): Количество ингредиента в рецепте
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_relations',
        verbose_name='Связанный рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_relations',
        verbose_name='Связанный ингредиент'
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} / {self.ingredient} - {self.amount}'


class Shopping_cart(models.Model):
    """Модель корзины покупок пользователя

    Attributes:
        user (ForeignKey): Пользователь - владелец корзины
        recipe (ForeignKey): Рецепт, добавленный в корзину покупок
    """
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Владелец корзины'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_carts',
        verbose_name='Рецепт в корзине'
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} | {self.recipe}'
