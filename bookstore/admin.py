"""
Register models with Django Admin.
Visit http://127.0.0.1:8000/admin/ to manage data via UI.
"""
from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'created_at']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'price', 'is_available', 'published_year']
    list_filter = ['genre', 'is_available']
    search_fields = ['title', 'isbn', 'author__name']
    list_editable = ['is_available', 'price']
