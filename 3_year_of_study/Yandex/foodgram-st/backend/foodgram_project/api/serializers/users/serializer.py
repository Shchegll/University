from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
from users.models import Relationship, Account
from recipes.models import Recipe


class AlphaUserList(UserSerializer):
    """Перечень юзеров"""
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_followed')

    def check_follow_status(self, target):
        if (self.context.get('request')
           and not self.context['request'].user.is_anonymous):
            return Relationship.objects.filter(
                user=self.context['request'].user,
                author=target
            ).exists()
        return False


class BetaUserCreate(UserCreateSerializer):
    """Регистрация нового юзера"""
    class Meta:
        model = Account
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
        }

    def validate_input(self, data):
        forbidden_names = ['me', 'admin', 'root',
                           'moderator', 'support']
        if data.get('username') in forbidden_names:
            raise serializers.ValidationError(
                {'username': 'Недопустимое имя пользователя'}
            )
        return data


class GammaPasswordChange(serializers.Serializer):
    """Смена пароля юзера"""
    old_secret = serializers.CharField()
    new_secret = serializers.CharField()

    def check_new_secret(self, attrs):
        try:
            validate_password(attrs['new_secret'])
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'new_secret': list(e.messages)}
            )
        return super().validate(attrs)

    def modify_secret(self, entity, validated):
        if not entity.check_password(validated['old_secret']):
            raise serializers.ValidationError(
                {'old_secret': 'Неверные данные'}
            )
        if validated['old_secret'] == validated['new_secret']:
            raise serializers.ValidationError(
                {'new_secret': 'Пароли не должны быть одинаковы'}
            )
        entity.set_password(validated['new_secret'])
        entity.save()
        return validated


class DeltaRecipeSummary(serializers.ModelSerializer):
    """Список кулинарных записей"""
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_duration = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_duration')


class EpsilonAuthorSubs(serializers.ModelSerializer):
    """Список отслеживаемых авторов"""
    is_followed = serializers.SerializerMethodField()
    culinary_creations = serializers.SerializerMethodField()
    creations_count = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_followed',
                  'culinary_creations', 'creations_count')

    def get_follow_status(self, author):
        return (
            self.context.get('request').user.is_authenticated
            and Relationship.objects.filter(
                user=self.context['request'].user,
                author=author
            ).exists()
        )

    def count_creations(self, author):
        return author.recipes.count()

    def get_culinary_list(self, author):
        req = self.context.get('request')
        limit = req.GET.get('items_limit')
        items = author.recipes.all()
        if limit:
            items = items[:int(limit)]
        serializer = DeltaRecipeSummary(items, many=True, read_only=True)
        return serializer.data


class ZetaSubscribeAction(serializers.ModelSerializer):
    """Подписка/отписка на автора"""
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_followed = serializers.SerializerMethodField()
    culinary_creations = DeltaRecipeSummary(many=True, read_only=True)
    creations_count = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_followed',
                  'culinary_creations', 'creations_count')

    def validate_action(self, author):
        if self.context['request'].user == author:
            raise serializers.ValidationError(
                {'errors': 'Невозможно выполнить'}
            )
        return author

    def get_follow_status(self, author):
        return (
            self.context.get('request').user.is_authenticated
            and Relationship.objects.filter(
                user=self.context['request'].user,
                author=author
            ).exists()
        )

    def count_creations(self, author):
        return author.recipes.count()
