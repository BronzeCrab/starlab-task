from books.models import Book, Author
from rest_framework import serializers


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = (
            "id",
            "name",
        )


class BookSerializer(serializers.HyperlinkedModelSerializer):

    authors = AuthorSerializer(many=True)

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "genre": instance.genre,
            "date_published": instance.date_published,
            "book_file": (
                instance.book_file.url
                if (instance.book_file and not instance.is_denied)
                else None
            ),
            "is_denied": instance.is_denied,
        }

    def create(self, validated_data: dict):
        authors_data = validated_data.pop("authors")
        book = Book(
            title=validated_data["title"],
            genre=validated_data["genre"],
            date_published=validated_data["date_published"],
        )
        book.save()
        self.get_or_create_authors(book, authors_data)
        return book

    def get_or_create_authors(self, new_book: Book, authors_data: list[dict]):
        """Создаем все указаных авторов (или получаем уже созданные)
        и добавляем к ним созданную Книгу."""
        for author_dict in authors_data:
            author, _ = Author.objects.get_or_create(name=author_dict["name"])
            author.books.add(new_book)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "genre",
            "date_published",
            "authors",
            "is_denied",
        )
