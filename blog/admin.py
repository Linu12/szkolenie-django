from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'tytul',
        'autor',
        'data_publikacji',
        'data_modyfikacji',
        'opublikowany',
    )

    readonly_fields = (
        'data_publikacji',
        'data_modyfikacji',
    )

    search_fields = ('tytul', 'tresc', 'autor')