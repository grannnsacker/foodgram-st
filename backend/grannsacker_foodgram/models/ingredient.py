from django.db import models


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200, db_index=True)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'
