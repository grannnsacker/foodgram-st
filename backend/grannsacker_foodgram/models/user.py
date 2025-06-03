from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

from grannsacker_foodgram.consts import MAX_CHAR_LEN

from django.contrib.auth.validators import UnicodeUsernameValidator

from grannsacker_foodgram.validators import forbidden_words_validator, only_letters_validator


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=MAX_CHAR_LEN,
        unique=True,
        help_text="Укажите действующий email — он будет использоваться для входа",
        error_messages={"unique": "Пользователь с таким email уже зарегистрирован"},
    )
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=MAX_CHAR_LEN,
        unique=True,
        help_text="Уникальное имя пользователя для авторизации",
        validators=[
            UnicodeUsernameValidator(),
            forbidden_words_validator,
        ],
        error_messages={
            "unique": "Пользователь с таким именем уже существует",
            "bad_word": "Нельзя использовать данное слова для юзернейма",
        },
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=MAX_CHAR_LEN,
        help_text="Ваше имя",
        validators=[
            forbidden_words_validator,
            only_letters_validator,
        ],
        error_messages={
            "bad_word": "Нельзя использовать данное слова для имени",
        },
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=MAX_CHAR_LEN,
        help_text="Ваша фамилия",
        validators=[
            forbidden_words_validator,
            only_letters_validator,
        ],
        error_messages={
            "bad_word": "Нельзя использовать данное слова для фамилии",
        },
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="avatars/",
        null=True,
        blank=True,
        help_text="Загрузите изображение профиля (необязательно)"
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]
