from rest_framework import serializers

from api.text import ERROR_REC_ALREADY_IS_IN_FAV
from grannsacker_foodgram.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(ERROR_REC_ALREADY_IS_IN_FAV)
        return data
