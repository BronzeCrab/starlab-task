from django.test import TestCase
from rest_framework.test import APIClient

from books.models import Book, Author


class BooksTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_migrations_are_ok(self):
        """Проверяем как отрабатывает миграция.
        Создаются ли тестовые записи в бд."""
        books_count = Book.objects.count()
        authors_count = Author.objects.count()
        assert books_count == 2
        assert authors_count == 0
