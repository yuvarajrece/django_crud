"""
Models for the Bookstore app.

A Django model maps directly to a PostgreSQL table.
Each attribute = a column in the database.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    """Represents an author in the database."""

    # CharField → VARCHAR in PostgreSQL
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)

    # DateField → DATE column
    birth_date = models.DateField(blank=True, null=True)

    # auto_now_add → set once on creation; auto_now → updated on every save
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']         # default ordering for querysets
        db_table = 'authors'        # explicit table name in PostgreSQL

    def __str__(self):
        return self.name            # shown in Django admin & shell


class Book(models.Model):
    """Represents a book. Linked to Author via a ForeignKey."""

    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('technology', 'Technology'),
        ('biography', 'Biography'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=300)

    # ForeignKey → one Author can have many Books
    # on_delete=CASCADE → deleting an author deletes their books too
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'        # author.books.all() ← reverse lookup
    )

    # DecimalField → NUMERIC in PostgreSQL (exact, unlike FloatField)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='other')
    published_year = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(2100)]
    )
    isbn = models.CharField(max_length=13, unique=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'books'

    def __str__(self):
        return f"{self.title} by {self.author.name}"
