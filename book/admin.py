from django.contrib import admin
from django.utils.safestring import mark_safe

from book.models import Book, BookImage, Category, Genre, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class BookImageStackedInline(admin.TabularInline):

    model = BookImage
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author_book', 'category', 'is_published', 'get_image')
    list_display_links = ('id', 'name',)
    list_filter = ('category', 'tags', 'genres','user', 'is_published',)
    search_fields = ('name', 'description', 'content', 'author_book')
    readonly_fields = ('created_at', 'updated_at', 'get_big_image',)
    inlines = [BookImageStackedInline,]

    @admin.display(description='Изображение')
    def get_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="150px">')
        return '-'

    @admin.display(description='Изображение')
    def get_big_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="100%">')
        return '-'





# Register your models here.
