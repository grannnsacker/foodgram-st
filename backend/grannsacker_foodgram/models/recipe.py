from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from grannsacker_foodgram.consts import MAX_CHAR_LEN, MIN_TIME_COOK, MAX_TIME_COOK
from grannsacker_foodgram.models import Ingredient

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField('Название рецепта', max_length=MAX_CHAR_LEN)
    image = models.ImageField('Изображение рецепта', upload_to='recipes/')
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты для рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                MIN_TIME_COOK,
                f'Время приготовления должно быть не менее {MIN_TIME_COOK} минуты',
            ),
            MinValueValidator(
                MAX_TIME_COOK,
                f'Время приготовления должно быть не менее {MAX_TIME_COOK} минуты',
            ),
        ],
    )
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at', 'name']
