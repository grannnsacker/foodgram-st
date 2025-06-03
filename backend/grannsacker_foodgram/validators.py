import re

from django.core.exceptions import ValidationError

from grannsacker_foodgram.consts import FORBIDDEN_WORDS


def forbidden_words_validator(value):
    lowered = value.lower()
    if lowered in FORBIDDEN_WORDS:
        raise ValidationError(
            f'Имя пользователя "{value}" запрещено',
            code="invalid_username",
        )


def only_letters_validator(value):
    if not re.fullmatch(r'[A-Za-zА-Яа-яЁё]+', value):
        raise ValidationError('Поле должно содержать только буквы')