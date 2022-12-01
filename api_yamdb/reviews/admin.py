"""Настройки админ-панели приложения Reviews."""

from django.contrib import admin

from .models import Title, Genre, Category


class TitleAdmin(admin.ModelAdmin):
    """Описание для моделей Title."""

    list_display = (
        'pk',
        'name',
        'year',
        'category',
        'genres',
        'description',
    )
    search_fields = ('name',)
    list_editable = ('category',)
    list_filter = ('category', 'year')
    empty_value_display = '-empty-'

    def genres(self, obj):
        """Отображение жанров."""
        return ", ".join([x.name for x in obj.genre.all()])


class GenreAdmin(admin.ModelAdmin):
    """Описание для моделей Genre."""

    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    empty_value_display = '-empty-'


class CategoryAdmin(admin.ModelAdmin):
    """Описание для моделей Category."""

    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)
    empty_value_display = '-empty-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre)
admin.site.register(Category)
