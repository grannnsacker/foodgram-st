from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied

from grannsacker_foodgram.models import Recipe, Favorite, Cart

from api.serializers import (
    RecipeSerializer,
    RecipeCreateSerializer,
    FavoriteSerializer,
    CartSerializer,
    RecipeLinkSerializer,
    ShortRecipeSerializer,
)
from api.filters import RecipeFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.author != request.user:
            raise PermissionDenied('Вы не можете изменять чужие рецепты')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.author != request.user:
            raise PermissionDenied('Вы не можете удалять чужие рецепты')
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data={'user': user.id, 'recipe': recipe.id},
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                ShortRecipeSerializer(recipe, context={'request': request}).data,
                status=status.HTTP_201_CREATED,
            )

        is_delete, _ = Favorite.objects.filter(user=user, recipe=recipe).delete()
        if is_delete:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            serializer = CartSerializer(
                data={'user': user.id, 'recipe': recipe.id},
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                ShortRecipeSerializer(recipe, context={'request': request}).data,
                status=status.HTTP_201_CREATED,
            )

        is_delete, _ = Cart.objects.filter(user=user, recipe=recipe).delete()
        if is_delete:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        recipes = Recipe.objects.filter(cart_by__user=user)

        ingredients = {}
        for recipe in recipes:
            for ingredient in recipe.ingredients.all():
                amount = recipe.recipe_ingredients.get(ingredient=ingredient).amount
                if ingredient.id in ingredients:
                    ingredients[ingredient.id]['amount'] += amount
                else:
                    ingredients[ingredient.id] = {
                        'name': ingredient.name,
                        'measurement_unit': ingredient.measurement_unit,
                        'amount': amount,
                    }

        shopping_list = ['Список покупок:\n']
        for ingredient in ingredients.values():
            shopping_list.append(
                f"• {ingredient['name']} ({ingredient['measurement_unit']}) - "
                f"{ingredient['amount']}"
            )
        return Response(
            '\n'.join(shopping_list),
            content_type='text/plain',
            headers={
                'Content-Disposition': 'attachment; filename="shopping_list.txt"'
            }
        )

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeLinkSerializer(
            {'short-link': request.build_absolute_uri(f'/recipes/{recipe.id}/')}
        )
        return Response(serializer.data)
