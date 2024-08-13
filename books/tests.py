from django.test import TestCase
from rest_framework.test import APIClient

from books.models import Book, Author


class BooksTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_migrations_are_ok(self):
        """Проверяем как отрабатывает миграция.
        Создаются ли тестовые записи в бд."""
        books = Book.objects.all()
        authors = Author.objects.all()
        assert len(books) == 2
        assert len(authors) == 0
