"""
Views handle HTTP requests and return responses.

We use DRF's ViewSets which automatically provide:
  GET    /api/books/        → list()
  POST   /api/books/        → create()
  GET    /api/books/{id}/   → retrieve()
  PUT    /api/books/{id}/   → update()
  PATCH  /api/books/{id}/   → partial_update()
  DELETE /api/books/{id}/   → destroy()
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, BookDetailSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Authors.
    ModelViewSet gives all 5 operations for free.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    # Enable ?search=<term> query param
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'created_at']

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """
        Custom action: GET /api/authors/{id}/books/
        Returns all books by a specific author.
        """
        author = self.get_object()
        books = author.books.all()
        serializer = BookDetailSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Books.
    Uses different serializers for read vs write operations.
    """
    queryset = Book.objects.select_related('author').all()

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'isbn', 'author__name']
    ordering_fields = ['title', 'price', 'published_year', 'created_at']

    def get_serializer_class(self):
        """
        Use detailed serializer for GET, simple one for POST/PUT/PATCH.
        This is a common DRF pattern.
        """
        if self.action in ['list', 'retrieve']:
            return BookDetailSerializer
        return BookSerializer

    def create(self, request, *args, **kwargs):
        """
        POST /api/books/
        Override to return 201 with detail serializer after creation.
        """
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()

        # Return the full detail view of the newly created book
        detail = BookDetailSerializer(book)
        return Response(detail.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Custom action: GET /api/books/available/
        Returns only books that are currently available.
        """
        books = Book.objects.filter(is_available=True).select_related('author')
        serializer = BookDetailSerializer(books, many=True)
        return Response({
            'count': books.count(),
            'results': serializer.data
        })

    @action(detail=True, methods=['patch'])
    def toggle_availability(self, request, pk=None):
        """
        Custom action: PATCH /api/books/{id}/toggle_availability/
        Flips the is_available flag.
        """
        book = self.get_object()
        book.is_available = not book.is_available
        book.save()
        return Response({
            'id': book.id,
            'title': book.title,
            'is_available': book.is_available
        })
