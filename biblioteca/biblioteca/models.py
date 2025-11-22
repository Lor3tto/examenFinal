from django.db import models
from django.core.exceptions import ValidationError

class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    stock = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']  # This fixes the pagination warning

    def clean(self):
        if self.stock < 0:
            raise ValidationError({'stock': 'Stock cannot be negative'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title