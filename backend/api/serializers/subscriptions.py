from django.contrib.auth import get_user_model

from api.serializers import ShortRecipeSerializer
from rest_framework import serializers

from grannsacker_foodgram.models import Recipe

User = get_user_model()


class SubscriptionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar',
        )


    def get_recipes(self, user):
        request  = self.context.get('request')
        recipes = Recipe.objects.filter(author=user)

        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            try:
                recipes = recipes[:int(recipes_limit)]
            except ValueError:
                pass

        serializer = ShortRecipeSerializer(recipes, many=True, context=self.context)
        return serializer.data

    def get_recipes_count(self, user):
        return Recipe.objects.filter(author=user).count()

    def get_is_subscribed(self, user):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.follower.filter(author=user).exists()
        return False
