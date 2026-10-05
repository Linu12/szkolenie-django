from django.contrib import admin
from .models import Post, Kategoria, Tag

admin.site.register(Kategoria)
admin.site.register(Tag)

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

    ordering = ('-data_publikacji',)