import pytest
from django.core.exceptions import ValidationError

from grannsacker_foodgram.consts import FORBIDDEN_WORDS
from grannsacker_foodgram.validators import forbidden_words_validator, only_letters_validator


@pytest.mark.parametrize("value", FORBIDDEN_WORDS)
def test_forbidden_words_validator_raises(value):
    with pytest.raises(ValidationError) as excinfo:
        forbidden_words_validator(value)
    assert f'Имя пользователя "{value}" запрещено' in str(excinfo.value)


@pytest.mark.parametrize("value", ['user', 'hello', 'тест', 'Пользователь'])
def test_forbidden_words_validator_passes(value):
    forbidden_words_validator(value)


@pytest.mark.parametrize("value", ['abc', 'Привет', 'Ёжик'])
def test_only_letters_validator_passes(value):
    only_letters_validator(value)


@pytest.mark.parametrize("value", ['abc123', 'hello!', 'test_1', 'привет2', 'abc def', ''])
def test_only_letters_validator_raises(value):
    with pytest.raises(ValidationError) as excinfo:
        only_letters_validator(value)
    assert 'Поле должно содержать только буквы' in str(excinfo.value)
