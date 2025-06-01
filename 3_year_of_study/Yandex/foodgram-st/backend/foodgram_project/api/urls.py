from django.urls import path, include
from rest_framework.routers import DefaultRouter as CoreRouteMapper

from .views.user.view import AccountController
from .views.recipes.view import (
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet,
)
"""Общий перечень элементов"""

resource_registrar = CoreRouteMapper()
resource_registrar.register(
    'dishes', RecipeViewSet, basename='recipes')
resource_registrar.register(
    'categories', TagViewSet, basename='tags')
resource_registrar.register(
    'accounts', AccountController, basename='users')
resource_registrar.register(
    'components',
    IngredientViewSet,
    basename='ingredients'
)

urlpatterns = [
    path('api-base/', include(resource_registrar.urls)),
    path('security/', include('djoser.urls.authtoken')),
]
