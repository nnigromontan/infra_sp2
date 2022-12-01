"""Миксины приложения api."""

from rest_framework import viewsets, mixins


class CreateListDestroyMixinViewset(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    """Кастомный миксин для настройки представлений."""

    pass
