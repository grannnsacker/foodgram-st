from django.contrib.auth import get_user_model
from django.db import models
from grannsacker_foodgram.models import Recipe

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
        help_text='Пользователь, которому принадлежит корзина',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart_by',
        verbose_name='Рецепт',
        help_text='Рецепт, добавленный в корзину',
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
        help_text='Когда рецепт был добавлен в корзину',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ['-added_at', 'user']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique_favorite')
        ]
