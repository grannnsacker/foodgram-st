from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from grannsacker_foodgram.consts import MAX_AMOUNT, MIN_AMOUNT
from grannsacker_foodgram.models import Recipe, Ingredient

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
        help_text='Рецепт, к которому относится ингредиент',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
        help_text='Ингредиент, используемый в рецепте',
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                f'Количество должно быть не менее {MIN_AMOUNT}',
            ),
            MaxValueValidator(
                MAX_AMOUNT,
                f'Количество должно быть не более {MAX_AMOUNT}',
            ),
        ],
        help_text='Количество ингредиентов, необходимое для рецепта',
        default=MIN_AMOUNT,
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ['recipe', 'ingredient']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique_recipe_ingredient'
            )
        ]
