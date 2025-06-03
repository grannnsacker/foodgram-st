from django.db import models
from grannsacker_foodgram.consts import MAX_CHAR_LEN, MIN_INGR_CHAR_LEN, MAX_INGR_CHAR_LEN, MIN_CHAR_LEN


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=MAX_CHAR_LEN,
        db_index=True,
        help_text='Название ингредиента',
        unique=True,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_INGR_CHAR_LEN,
        help_text='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

