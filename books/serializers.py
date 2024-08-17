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
            'title': instance.title,
            'genre': instance.genre,
        }
        
    def create(self, validated_data: dict):
        authors_data = validated_data.pop('authors')
        book = Book(title=validated_data["title"], genre=validated_data["genre"])
        book.save()
        for author_dict in authors_data:
            self.get_or_create_author(book, author_dict)
        return book

    def get_or_create_author(self, new_book: Book, author_dict: dict):
        author, _ = Author.objects.get_or_create(name=author_dict["name"])
        author.books.add(new_book)

    class Meta:
        model = Book
        fields = ["id", "title", "date_published", "genre", "authors"]
