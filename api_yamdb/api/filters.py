"""Фильтры приложения api."""

from django_filters import CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    """Класс, в котором описаны настройки фильтрации моделей Title."""

    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(lookup_expr='contains')

    class Meta:
        """Класс Meta, хранящий информацию полях модели Title."""

        model = Title
        fields = ('year', 'name', 'category', 'genre')
