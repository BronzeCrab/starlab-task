from books.models import Book, Author
from rest_framework import serializers


class BookSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.CharField(required=True)

    class Meta:
        model = Book
        fields = ["id", "title", "date_published", "genre", "author"]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name"]
