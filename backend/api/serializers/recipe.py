from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from api.text import (
    ERROR_IMG_CANT_BE_EMPTY,
    ERROR_ADD_AT_LEAST_ONE,
    ERROR_INGR_MUST_BE_UNIQ, ERROR_FAKE_INGR,
)
from api.utils import format_doesnt_exist_ingr
from grannsacker_foodgram.models import (
    Recipe,
    Ingredient,
    Favorite,
    Cart,
    RecipeIngredient,
)
from api.serializers import UserSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientSerializerWrite(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(required=True, min_value=1, max_value=999)


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients', many=True, read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Cart.objects.filter(user=request.user, recipe=obj).exists()
        return False


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializerWrite(many=True)
    image = Base64ImageField(required=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        if not data.get('image'):
            raise serializers.ValidationError(
                {'image': ERROR_IMG_CANT_BE_EMPTY}
            )

        ingredients = data.get('ingredients')
        if not ingredients or len(ingredients) == 0:
            raise serializers.ValidationError(ERROR_ADD_AT_LEAST_ONE)


        ids = [item['id'] for item in ingredients]
        if len(set(ids)) < len(ids):
            raise serializers.ValidationError(ERROR_INGR_MUST_BE_UNIQ)

        found_ids = set(Ingredient.objects.filter(id__in=ids).values_list('id', flat=True))
        if set(ids) - found_ids:
            raise serializers.ValidationError(
                {'ingredients': ERROR_FAKE_INGR}
            )

        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        new_recipe = Recipe.objects.create(**validated_data)
        associations = [
            RecipeIngredient(
                recipe=new_recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(associations)

        return new_recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if ingredients is not None:
            instance.ingredients.clear()
            links = [
                RecipeIngredient(
                    recipe=instance,
                    ingredient_id=ing['id'],
                    amount=ing['amount']
                )
                for ing in ingredients
            ]
            RecipeIngredient.objects.bulk_create(links)

        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data

class RecipeLinkSerializer(serializers.Serializer):
    link = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        return instance
