from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'author', 'published_date', 'stock']
        
    def validate_stock(self, value):
        """Validate that stock is not negative"""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value
    
    def validate_isbn(self, value):
        """Validate ISBN format and uniqueness"""
        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 characters long")
        return value
