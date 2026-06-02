"""
Serializers convert Django model instances ↔ JSON.

Think of them as the translation layer between
your Python objects and what the API sends/receives.
"""
from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model."""

    # Read-only computed field — not stored in DB
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        # Which fields to expose in the API
        fields = ['id', 'name', 'bio', 'birth_date', 'book_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_book_count(self, obj):
        """Count how many books this author has."""
        return obj.books.count()


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model — used for CREATE / UPDATE."""

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'price', 'genre',
            'published_year', 'isbn', 'is_available', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class BookDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model — used for READ (GET).
    Shows nested author details instead of just the author ID.
    """

    # Nested serializer → expands the author FK into full object
    author = AuthorSerializer(read_only=True)

    # author_id lets us still accept an author ID when writing
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_id', 'price', 'genre',
            'published_year', 'isbn', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
