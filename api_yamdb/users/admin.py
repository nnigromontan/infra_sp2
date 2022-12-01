from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'date_joined',
        'is_superuser'
    )
    search_fields = ('username',)
    list_filter = ('date_joined',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
