"""
URL routing for the Bookstore API.

DRF Router automatically creates all URL patterns for a ViewSet.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register our ViewSets
router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'books', views.BookViewSet, basename='book')

# The router generates these URLs automatically:
#   /api/authors/                     GET (list), POST (create)
#   /api/authors/{id}/                GET (retrieve), PUT, PATCH, DELETE
#   /api/authors/{id}/books/          GET (custom action)
#   /api/books/                       GET (list), POST (create)
#   /api/books/{id}/                  GET (retrieve), PUT, PATCH, DELETE
#   /api/books/available/             GET (custom action)
#   /api/books/{id}/toggle_availability/  PATCH (custom action)

urlpatterns = [
    path('', include(router.urls)),
]
