from rest_framework import serializers

from api.text import ERROR_REC_ALREADY_IS_IN_CART
from grannsacker_foodgram.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']
        if Cart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(ERROR_REC_ALREADY_IS_IN_CART)
        return data
