from django.contrib.auth import get_user_model
from django_filters import (BooleanFilter, CharFilter, FilterSet,
                            ModelChoiceFilter, ModelMultipleChoiceFilter)

from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class RecipeFilter(FilterSet):
    """Фильтр для рецептов"""
    is_favorited = BooleanFilter(
        field_name='add_favorites__user',
        method='filter_is_favorited'
    )
    is_in_shopping_cart = BooleanFilter(
        field_name='add_shoppingcart__user',
        method='filter_is_in_shopping_cart'
    )
    author = ModelChoiceFilter(
        field_name='author', queryset=User.objects.all()
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug', queryset=Tag.objects.all(),
        to_field_name='slug'
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'author', 'tags',)

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(add_favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(add_shoppingcart__user=self.request.user)
        return queryset


class IngredientFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='startswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
