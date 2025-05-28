from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from grannsacker_foodgram.models import Ingredient
from grannsacker_foodgram.serializers import IngredientSerializer
from grannsacker_foodgram.filters import IngredientFilter


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [IngredientFilter]
    search_fields = ['^name']