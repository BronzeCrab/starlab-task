from books.models import Book, Author
from rest_framework import serializers


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ["id", "name"]


class BookSerializer(serializers.HyperlinkedModelSerializer):

    authors = AuthorSerializer(many=True)

    def to_representation(self, instance):
        return {
            "title": instance.title,
            "genre": instance.genre,
        }

    def create(self, validated_data: dict):
        authors_data = validated_data.pop("authors")
        book = Book(title=validated_data["title"], genre=validated_data["genre"])
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
        fields = ["id", "title", "date_published", "genre", "authors"]
