from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

EMPTY_VAL = '---'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'pub_date', 'author', 'text', 'score')
    search_fields = ('text',)
    list_filter = ('pub_date', 'score')
    empty_value_display = EMPTY_VAL


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review_id', 'pub_date', 'author', 'text')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')
    empty_value_display = EMPTY_VAL


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name')
    empty_value_display = EMPTY_VAL


@admin.register(Genre)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name')
    empty_value_display = EMPTY_VAL


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')
    empty_value_display = EMPTY_VAL
