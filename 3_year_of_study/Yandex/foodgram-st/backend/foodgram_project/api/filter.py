from django_filters.rest_framework import filters, FilterSet
from recipes.models import Recipe, Tag_my


class CustomRecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag_my.objects.all()
    )
    favorited = filters.BooleanFilter(
        method='check_favorited_status')
    in_shopping_list = filters.BooleanFilter(
        method='check_shopping_status')

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def check_favorited_status(self, queryset, name, value):
        current_user = self.request.user
        if value and current_user.is_authenticated:
            return queryset.filter(favorite_recipe__user=current_user)
        return queryset

    def check_shopping_status(self, queryset, name, value):
        current_user = self.request.user
        if value and current_user.is_authenticated:
            return queryset.filter(shopping_recipe__user=current_user)
        return queryset
