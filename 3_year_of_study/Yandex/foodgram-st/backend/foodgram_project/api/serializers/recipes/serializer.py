from drf_base64.fields import Base64ImageField
from api.serializers.users.serializer import AlphaUserList
from recipes.models import (Favor, Ingredient, Recipe, Recipe_ing,
                            Shopping_cart, Tag_my)
from django.db import transaction
from rest_framework import serializers


class ElementSerializer(serializers.ModelSerializer):
    """Общий перечень элементов"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Общий список категорий"""
    class Meta:
        model = Tag_my
        fields = '__all__'


class FormulaComponentSerializer(serializers.ModelSerializer):
    """Составляющие формулы с количеством"""
    element_id = serializers.ReadOnlyField(source='ingredient.id')
    element_name = serializers.ReadOnlyField(source='ingredient.name')
    unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Recipe_ing
        fields = ('element_id', 'element_name',
                  'unit', 'amount')


class FormulaDetailSerializer(serializers.ModelSerializer):
    """Детали формулы"""
    creator = AlphaUserList(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    components = FormulaComponentSerializer(
        many=True, read_only=True, source='recipes')
    is_bookmarked = serializers.SerializerMethodField()
    is_in_kitchen_list = serializers.SerializerMethodField()
    image_data = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'categories',
                  'creator', 'components',
                  'is_bookmarked', 'is_in_kitchen_list',
                  'title', 'image_data',
                  'description', 'prep_duration')

    def check_bookmark_status(self, formula):
        return (
            self.context.get('request').user.is_authenticated
            and Favor.objects.filter(
                user=self.context['request'].user,
                recipe=formula).exists()
        )

    def check_kitchen_list_status(self, formula):
        return (
            self.context.get('request').user.is_authenticated
            and Shopping_cart.objects.filter(
                user=self.context['request'].user,
                recipe=formula).exists()
        )


class ComponentCreateSerializer(serializers.ModelSerializer):
    """Элемент и количество для создания формулы"""
    element_id = serializers.IntegerField()

    class Meta:
        model = Recipe_ing
        fields = ('element_id', 'amount')


class FormulaEditSerializer(serializers.ModelSerializer):
    """Создание, изменение и удаление формулы"""
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag_my.objects.all()
    )
    creator = AlphaUserList(read_only=True)
    identifier = serializers.ReadOnlyField()
    components = ComponentCreateSerializer(many=True)
    image_data = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('identifier', 'components',
                  'categories', 'image_data',
                  'title', 'description',
                  'prep_duration', 'creator')
        extra_kwargs = {
            'components': {'required': True, 'allow_blank': False},
            'categories': {'required': True, 'allow_blank': False},
            'title': {'required': True, 'allow_blank': False},
            'description': {'required': True, 'allow_blank': False},
            'image_data': {'required': True, 'allow_blank': False},
            'prep_duration': {'required': True},
        }

    def validate_input(self, data):
        required_fields = ['title', 'description', 'prep_duration']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(
                    f'{field} - обязательное поле.'
                )
        if not data.get('categories'):
            raise serializers.ValidationError(
                'Требуется указать мин одну категорию'
            )
        if not data.get('components'):
            raise serializers.ValidationError(
                'Требуется указать мин один компонент'
            )
        component_ids = [item['element_id'] for item in data.get('components')]
        if len(component_ids) != len(set(component_ids)):
            raise serializers.ValidationError(
                'Компоненты не должны повторяться'
            )
        return data

    @transaction.atomic
    def link_components_categories(self, formula, categories, components):
        formula.categories.set(categories)
        Recipe_ing.objects.bulk_create(
            [Recipe_ing(
                recipe=formula,
                ingredient=Ingredient.objects.get(pk=component['element_id']),
                amount=component['amount']
            ) for component in components]
        )

    @transaction.atomic
    def build_formula(self, validated):
        categories = validated.pop('categories')
        components = validated.pop('components')
        formula = Recipe.objects.create(
            creator=self.context['request'].user,
            **validated
        )
        self.link_components_categories(formula, categories, components)
        return formula

    @transaction.atomic
    def modify_formula(self, instance, validated):
        instance.image_data = validated.get('image_data', instance.image_data)
        instance.title = validated.get('title', instance.title)
        instance.description = validated.get(
            'description', instance.description)
        instance.prep_duration = validated.get(
            'prep_duration', instance.prep_duration)
        categories = validated.pop('categories')
        components = validated.pop('components')
        Recipe_ing.objects.filter(
            recipe=instance,
            ingredient__in=instance.ingredients.all()).delete()
        self.link_components_categories(instance, categories, components)
        instance.save()
        return instance

    def represent_formula(self, instance):
        return FormulaDetailSerializer(instance,
                                       context=self.context).data
