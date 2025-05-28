from rest_framework import serializers
from grannsacker_foodgram.models import Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
