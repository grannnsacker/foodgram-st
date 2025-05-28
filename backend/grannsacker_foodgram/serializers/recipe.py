import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from grannsacker_foodgram.models import Recipe, Ingredient, Favorite, Cart, RecipeIngredient
from grannsacker_foodgram.serializers import UserSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Serializer for recipe ingredients with amount."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )

class RecipeIngredientSerializerWrite(serializers.Serializer):
    """Serializer for write recipe ingredients with amount."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField(required=True, min_value=1)



class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        many=True,
        read_only=True
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
            return Favorite.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Cart.objects.filter(
                user=request.user,
                recipe=obj
            ).exists()
        return False


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe in cart."""
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
    """Serializer for creating and updating recipes."""
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
            'cooking_time'
        )

    def validate(self, data):
        if not data.get('image'):
                raise serializers.ValidationError({'image': 'Поле image не может быть пустым'})

        ingredients = data.get('ingredients', [])
        if not ingredients:
            raise serializers.ValidationError(
                'Добавьте хотя бы один ингредиент'
            )

        ingredient_ids = [item['id'] for item in ingredients]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться'
            )

        # Check if all ingredients exist
        existing_ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
        if len(existing_ingredients) != len(ingredient_ids):
            found_ids = set(existing_ingredients.values_list('id', flat=True))
            missing_ids = set(ingredient_ids) - found_ids
            raise serializers.ValidationError(
                f'Ингредиенты с ID {missing_ids} не существуют'
            )

        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self._create_recipe_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self._create_recipe_ingredients(instance, ingredients_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


    def _create_recipe_ingredients(self, recipe, ingredients_data):
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient_id=item['id'],
                amount=item['amount']
            ) for item in ingredients_data
        ])



class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for favorites."""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное'
            )
        return data


class CartSerializer(serializers.ModelSerializer):
    """Serializer for cart."""
    class Meta:
        model = Cart
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe = data['recipe']
        if Cart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в список покупок'
            )
        return data


class RecipeLinkSerializer(serializers.Serializer):
    """Serializer for recipe link."""
    link = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        return instance