from django.contrib import admin
from .models import MenuItem


class MenuItemInline(admin.StackedInline):
    """
    Вложенная редактура пунктов меню в объекте меню.
    """
    model = MenuItem
    extra = 1


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Админ для пунктов меню.
    """
    list_display = ['name', 'url', 'named_url', 'parent']
    list_filter = ['name']
    ordering = ['name', 'id']
    search_fields = ['name']
