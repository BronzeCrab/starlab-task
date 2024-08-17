from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book, Author


class BooksTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username="afoobar")
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_migrations_are_ok(self):
        """Проверяем как отрабатывает миграция.
        Создаются ли тестовые записи в бд."""
        books = Book.objects.all()
        authors = Author.objects.all()
        assert len(books) == 2
        assert len(authors) == 1
        assert authors[0].books.count() == 2
        assert len(books[0].author_set.all()) == 1
        assert len(books[1].author_set.all()) == 1
        assert books[0].date_published
        assert not books[0].book_file

    def test_create_book_ok(self):
        """Созаем новую Book. Успешное создание книги и автора, автор указан."""
        amount_of_books = Book.objects.count()
        amount_of_authors = Author.objects.count()

        genre = "genre"
        author = "new_author"
        resp = self.client.post(
            "/books/", {"title": "title", "genre": genre, "author": author}
        )
        assert resp.status_code == status.HTTP_201_CREATED

        new_amount_of_books = Book.objects.count()
        assert new_amount_of_books == amount_of_books + 1

        a_book = Book.objects.last()
        assert a_book.genre == genre
        assert a_book.author_set.count() == 1
        assert a_book.author_set.first().name == author

        new_amount_of_authors = Author.objects.count()
        assert new_amount_of_authors == amount_of_authors + 1

    def test_create_book_failed(self):
        """Созаем новую Book. Не получается создать книгу
        и автора, автор не указан."""
        amount_of_books = Book.objects.count()
        amount_of_authors = Author.objects.count()

        genre = "genre"
        resp = self.client.post("/books/", {"title": "title", "genre": genre})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        new_amount_of_books = Book.objects.count()
        assert new_amount_of_books == amount_of_books

        new_amount_of_authors = Author.objects.count()
        assert new_amount_of_authors == amount_of_authors
