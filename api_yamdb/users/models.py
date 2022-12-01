from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


def get_random():
    return get_random_string(length=32)


USER = 'user'
MODER = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'user'),
    (MODER, 'moderator'),
    (ADMIN, 'admin'),
)


class User(AbstractUser):
    role = models.CharField(
        max_length=9,
        choices=ROLES,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        max_length=32, default=get_random
    )
    email = models.EmailField(_('email address'), blank=False, unique=True)
