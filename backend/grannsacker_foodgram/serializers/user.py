from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from grannsacker_foodgram.models import Recipe, Subscription
from rest_framework.validators import UniqueValidator
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer

User = get_user_model()


class UserCreateSerializer(DjoserUserCreateSerializer):
    """Serializer for user registration."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )


    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(DjoserUserSerializer):
    """Serializer for user data."""
    is_subscribed = serializers.SerializerMethodField()
    avatar = serializers.ImageField(use_url=True)
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.following.filter(user=request.user).exists()
        return False


class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, validated_data):
        """Change user password."""
        user = self.context['request'].user

        if not user.check_password(validated_data['current_password']):
            raise serializers.ValidationError({'current_password': 'Неверный текущий пароль'})
        return validated_data



class RecipeShortSerializer(serializers.ModelSerializer):
    """Short serializer for recipes in subscriptions."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(UserSerializer):
    """Serializer for user subscriptions."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return [
            {
                'id': recipe.id,
                'name': recipe.name,
                'image': recipe.image.url,
                'cooking_time': recipe.cooking_time
            } for recipe in recipes
        ]

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriptionsSerializer(serializers.ModelSerializer):
    """Serializer for user subscriptions list."""
    email = serializers.EmailField()
    id = serializers.IntegerField()
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
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar'
        )

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = Recipe.objects.filter(author=obj)
        recipes_limit = request.query_params.get('recipes_limit')
        
        if recipes_limit:
            try:
                recipes_limit = int(recipes_limit)
                recipes = recipes[:recipes_limit]
            except (TypeError, ValueError):
                pass
        
        return RecipeShortSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class ChangeAvatarSerializer(serializers.ModelSerializer):
    """Serializer for avatar."""
    avatar = Base64ImageField()
    class Meta:
        model = User
        fields = ('avatar',)


class SubscribeResponseSerializer(serializers.ModelSerializer):
    """Serializer for subscribe action response."""
    email = serializers.EmailField()
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_subscribed = serializers.BooleanField(default=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = serializers.ImageField(use_url=True)
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = Recipe.objects.filter(author=obj)
        recipes_limit = request.query_params.get('recipes_limit')
        
        if recipes_limit:
            try:
                recipes_limit = int(recipes_limit)
                recipes = recipes[:recipes_limit]
            except (TypeError, ValueError):
                pass
        
        return RecipeShortSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
