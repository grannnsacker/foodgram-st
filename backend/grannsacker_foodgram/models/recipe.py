from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from grannsacker_foodgram.models import Ingredient

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField('Название рецепта', max_length=200)
    image = models.ImageField('Изображение рецепта', upload_to='recipes/')
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты для рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        validators=[
            MinValueValidator(1, 'Время приготовления должно быть не менее 1 минуты')
        ],
    )
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at', 'name']

    def __str__(self):
        return self.name
