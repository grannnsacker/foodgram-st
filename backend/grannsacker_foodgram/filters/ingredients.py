from rest_framework.filters import SearchFilter
from grannsacker_foodgram.models import Ingredient


class IngredientFilter(SearchFilter):
    """Filter for Ingredient model."""
    search_param = 'name'
