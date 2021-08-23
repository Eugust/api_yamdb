from django.contrib import admin
from reviews.admin import EMPTY_VAL

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Manage DB users."""
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio',
        'confirmation_code',
    )
    search_fields = (
        'username',
        'email',
    )
    filter_fields = (
        'role',
    )
    empty_value_display = EMPTY_VAL
