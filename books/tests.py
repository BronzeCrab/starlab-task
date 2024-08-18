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
        assert len(books) == 3
        assert len(authors) == 2
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
            "/books/",
            {
                "title": "title",
                "genre": genre,
                "authors": [{"name": author}],
                "date_published": "2024-08-08",
            },
            format="json",
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

    def test_create_book_failed_no_author(self):
        """Созаем новую Book. Не получается создать книгу
        и автора, автор не указан."""
        amount_of_books = Book.objects.count()
        amount_of_authors = Author.objects.count()

        genre = "genre"
        resp = self.client.post(
            "/books/",
            {
                "title": "title",
                "genre": genre,
                "date_published": "2024-08-08",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.json() == {"authors": ["This field is required."]}

        new_amount_of_books = Book.objects.count()
        assert new_amount_of_books == amount_of_books

        new_amount_of_authors = Author.objects.count()
        assert new_amount_of_authors == amount_of_authors

    def test_create_book_failed_no_title(self):
        """Созаем новую Book. Не получается создать книгу
        и автора, название книги не указано."""
        amount_of_books = Book.objects.count()
        amount_of_authors = Author.objects.count()

        resp = self.client.post(
            "/books/",
            {
                "genre": "genre",
                "authors": [{"name": "new_author"}],
                "date_published": "2024-08-08",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.json() == {"title": ["This field is required."]}

        new_amount_of_books = Book.objects.count()
        assert new_amount_of_books == amount_of_books

        new_amount_of_authors = Author.objects.count()
        assert new_amount_of_authors == amount_of_authors

    def test_create_book_failed_no_date_published(self):
        """Созаем новую Book. Не получается создать книгу
        и автора, дата книги не указана."""
        amount_of_books = Book.objects.count()
        amount_of_authors = Author.objects.count()

        resp = self.client.post(
            "/books/",
            {
                "genre": "genre",
                "authors": [{"name": "new_author"}],
                "title": "new_title",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.json() == {"date_published": ["This field is required."]}

        new_amount_of_books = Book.objects.count()
        assert new_amount_of_books == amount_of_books

        new_amount_of_authors = Author.objects.count()
        assert new_amount_of_authors == amount_of_authors

    def test_get_all_books(self):
        """Получаем список всех Book."""
        resp = self.client.get("/books/")
        assert resp.status_code == status.HTTP_200_OK
        res = resp.json()

        amount_of_books = Book.objects.count()
        assert amount_of_books > 0
        assert len(res) == amount_of_books

    def test_get_one_book(self):
        """Получаем одну Book."""
        book_id = 1
        resp = self.client.get(f"/books/{book_id}/")
        assert resp.status_code == status.HTTP_200_OK

        res = resp.json()
        assert type(res) is dict
        assert res["title"] == f"book_{book_id}"
        assert res["is_denied"] is False
        assert res["book_file"] is None

    def test_update_one_book(self):
        """Обновляем один Book."""
        book_id = 1
        book = Book.objects.get(id=book_id)
        assert book.genre == "test_genre_1"

        resp = self.client.patch(f"/books/{book_id}/", {"genre": "new_genre"})
        assert resp.status_code == status.HTTP_200_OK

        res = resp.json()
        assert type(res) is dict
        assert res["title"] == f"book_{book_id}"

        book = Book.objects.get(id=book_id)
        assert book.genre == "new_genre"

    def test_delete_one_book(self):
        """Удаляем один Book. Список книг в
        Авторе должен также обновиться."""
        # это Автор был создан в начальной миграции:
        first_author = Author.objects.get(id=1)
        # эти книги тоже были созданы в начальной миграции:
        assert first_author.books.count() == 2

        amount_of_books = Book.objects.count()

        book_id = 1
        resp = self.client.delete(f"/books/{book_id}/")
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        new_amount_of_books = Book.objects.count()
        assert new_amount_of_books == amount_of_books - 1

        first_author = Author.objects.get(id=1)
        assert first_author.books.count() == 1

    def test_create_author(self):
        """Созаем новый Author."""
        amount_of_authors = Author.objects.count()

        resp = self.client.post("/authors/", {"name": "some_name"})
        assert resp.status_code == status.HTTP_201_CREATED

        new_amount_of_authors = Author.objects.count()

        assert new_amount_of_authors == amount_of_authors + 1
        assert Author.objects.last().name == "some_name"

    def test_get_all_authors(self):
        """Получаем список всех Author."""
        resp = self.client.get("/authors/")
        assert resp.status_code == status.HTTP_200_OK

        res = resp.json()

        amount_of_authors = Author.objects.count()
        assert amount_of_authors > 0
        assert len(res) == amount_of_authors
        assert res == [{"id": 1, "name": "Author1"}, {"id": 2, "name": "Frank Herbert"}]

    def test_get_one_author(self):
        """Получаем один Author."""
        author_id = 1
        resp = self.client.get(f"/authors/{author_id}/")
        assert resp.status_code == status.HTTP_200_OK

        res = resp.json()
        assert type(res) is dict
        assert res == {"id": 1, "name": "Author1"}

    def test_update_one_author(self):
        """Обновляем один Author."""
        new_name = "new_name_123"

        author_id = 1
        author = Author.objects.get(id=author_id)
        assert author.name != new_name

        resp = self.client.patch(f"/authors/{author_id}/", {"name": new_name})
        assert resp.status_code == status.HTTP_200_OK

        res = resp.json()
        assert type(res) is dict

        author = Author.objects.get(id=author_id)
        assert author.name == new_name

    def test_delete_one_author(self):
        """Удаляем один Author."""
        amount_of_authors = Author.objects.count()

        author_id = 1
        resp = self.client.delete(f"/authors/{author_id}/")
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        new_amount_of_authors = Author.objects.count()
        assert new_amount_of_authors == amount_of_authors - 1
