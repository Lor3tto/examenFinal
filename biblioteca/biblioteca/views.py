from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root - Shows all available endpoints
    """
    return Response({
        'books': reverse('book-list', request=request, format=format),
        'admin': request.build_absolute_uri('/admin/'),
        'endpoints': {
            'List all books (GET)': reverse('book-list', request=request, format=format),
            'Create book (POST)': reverse('book-list', request=request, format=format),
            'Retrieve book (GET)': reverse('book-list', request=request, format=format) + '{id}/',
            'Update book (PUT)': reverse('book-list', request=request, format=format) + '{id}/',
            'Partial update book (PATCH)': reverse('book-list', request=request, format=format) + '{id}/',
            'Delete book by ID (DELETE)': reverse('book-list', request=request, format=format) + '{id}/',
            'Delete book by ISBN (DELETE)': reverse('book-list', request=request, format=format) + 'delete-by-isbn/{isbn}/',
        },
        'filters': {
            'Filter by author': reverse('book-list', request=request, format=format) + '?author=AuthorName',
            'Search': reverse('book-list', request=request, format=format) + '?search=keyword',
            'Pagination': reverse('book-list', request=request, format=format) + '?page=2',
        }
    })

class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'author']
    
    def get_queryset(self):
        queryset = Book.objects.all()
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__icontains=author)
        return queryset
    
    @action(detail=False, methods=['delete'], url_path='delete-by-isbn/(?P<isbn>[^/.]+)')
    def delete_by_isbn(self, request, isbn=None):
        """
        Delete a book by ISBN
        URL: DELETE /api/books/delete-by-isbn/{isbn}/
        """
        try:
            book = get_object_or_404(Book, isbn=isbn)
            book.delete()
            return Response(
                {'message': f'Book with ISBN {isbn} has been deleted successfully.'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Book.DoesNotExist:
            return Response(
                {'error': f'Book with ISBN {isbn} not found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
