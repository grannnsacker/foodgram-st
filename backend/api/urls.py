from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    UserViewSet,
    IngredientsViewSet,
    RecipeViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("ingredients", IngredientsViewSet, basename="ingredients")
router.register("recipes", RecipeViewSet, basename="recipes")
router.register("shopping_cart", RecipeViewSet, basename="shopping_cart")
router.register(
    "download_shopping_cart", RecipeViewSet, basename="download_shopping_cart"
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
