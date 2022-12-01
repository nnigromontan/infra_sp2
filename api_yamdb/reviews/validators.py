"""Валидаторы приложения review."""

from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    """Валидатор года."""
    if value > timezone.now().year:
        raise ValidationError('Этот год еще не наступил')
