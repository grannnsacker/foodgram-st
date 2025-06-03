from django.contrib.auth import get_user_model
from django.db import models
from grannsacker_foodgram.models import Recipe
from django.utils.timezone import now


User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
        help_text='Пользователь, который добавил рецепт в избранное',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Рецепт',
        help_text='Рецепт, добавленный в избранное',
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
        help_text='Когда рецепт был добавлен в избранное',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['-added_at', 'user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite_recipe'
            )
        ]

