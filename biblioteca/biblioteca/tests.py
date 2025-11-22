from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import Book
from datetime import date

class BookModelTestCase(TestCase):
    def test_create_valid_book(self):
        """Test creating a valid book"""
        book = Book.objects.create(
            isbn='1234567890123',
            title='Test Book',
            author='Test Author',
            published_date=date.today(),
            stock=10
        )
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.stock, 10)

    def test_negative_stock_validation(self):
        """Test that negative stock raises ValidationError"""
        book = Book(
            isbn='1234567890123',
            title='Test Book',
            author='Test Author',
            published_date=date.today(),
            stock=-1
        )
        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_unique_isbn_constraint(self):
        """Test that duplicate ISBN raises error"""
        Book.objects.create(
            isbn='1234567890123',
            title='First Book',
            author='Author One',
            published_date=date.today(),
            stock=5
        )
        
        with self.assertRaises(Exception):
            Book.objects.create(
                isbn='1234567890123',
                title='Second Book',
                author='Author Two',
                published_date=date.today(),
                stock=3
            )

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            isbn='1234567890123',
            title='Django for Beginners',
            author='William Vincent',
            published_date=date(2020, 1, 1),
            stock=5
        )
        self.book2 = Book.objects.create(
            isbn='9876543210987',
            title='Python Crash Course',
            author='Eric Matthes',
            published_date=date(2019, 5, 15),
            stock=3
        )
        self.book3 = Book.objects.create(
            isbn='1111111111111',
            title='Two Scoops of Django',
            author='William Vincent',
            published_date=date(2021, 3, 10),
            stock=8
        )

    def test_create_valid_book_returns_201(self):
        """Test creating a valid book returns 201"""
        url = reverse('book-list')
        data = {
            'isbn': '2222222222222',
            'title': 'New Book',
            'author': 'New Author',
            'published_date': '2023-01-01',
            'stock': 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_create_duplicate_isbn_returns_400(self):
        """Test creating book with duplicate ISBN returns 400"""
        url = reverse('book-list')
        data = {
            'isbn': '1234567890123',  # Duplicate ISBN
            'title': 'Duplicate Book',
            'author': 'Some Author',
            'published_date': '2023-01-01',
            'stock': 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_negative_stock_returns_400(self):
        """Test creating book with negative stock returns 400"""
        url = reverse('book-list')
        data = {
            'isbn': '3333333333333',
            'title': 'Negative Stock Book',
            'author': 'Test Author',
            'published_date': '2023-01-01',
            'stock': -5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_paginated_list_returns_200(self):
        """Test getting paginated list returns 200 with pagination structure"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_filter_by_author(self):
        """Test filtering by author returns only books by that author"""
        url = reverse('book-list')
        response = self.client.get(url, {'author': 'William Vincent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        for book in response.data['results']:
            self.assertEqual(book['author'], 'William Vincent')

    def test_update_book_put_persists_changes(self):
        """Test updating book with PUT persists changes"""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        data = {
            'isbn': '1234567890123',
            'title': 'Updated Django Book',
            'author': 'William Vincent',
            'published_date': '2020-01-01',
            'stock': 15
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.title, 'Updated Django Book')
        self.assertEqual(updated_book.stock, 15)

    def test_partial_update_book_patch_persists_changes(self):
        """Test partial updating book with PATCH persists changes"""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        data = {'stock': 20}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.stock, 20)
        # Other fields should remain unchanged
        self.assertEqual(updated_book.title, 'Django for Beginners')

    def test_delete_book_returns_204_and_removes_book(self):
        """Test deleting book returns 204 and book no longer exists"""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book no longer exists
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book1.pk)
        
        self.assertEqual(Book.objects.count(), 2)

    def test_retrieve_single_book(self):
        """Test retrieving a single book"""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for Beginners')

    def test_pagination_page_size(self):
        """Test that pagination works with correct page size"""
        # Create more books to test pagination
        for i in range(15):
            Book.objects.create(
                isbn=f'{i+1000:013d}',  # Creates 13-digit ISBN
                title=f'Book {i}',
                author=f'Author {i}',
                published_date=date.today(),
                stock=i
            )
        
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Page size is 10
        self.assertIsNotNone(response.data['next'])  # Should have next page

    def test_delete_book_by_isbn_returns_204(self):
        """Test deleting book by ISBN returns 204 and book no longer exists"""
        isbn = self.book1.isbn
        url = f'/api/books/delete-by-isbn/{isbn}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book no longer exists
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(isbn=isbn)
        
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_nonexistent_isbn_returns_404(self):
        """Test deleting non-existent ISBN returns 404"""
        url = '/api/books/delete-by-isbn/9999999999999/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
