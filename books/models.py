from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    title = models.CharField(max_length=30)
    date_published = models.DateField(auto_now_add=True)
    genre = models.CharField(max_length=30)
    book_file = models.FileField()

    def __str__(self):
        return self.title


@receiver(post_save, sender=Book)
def get_or_create_author(sender, **kwargs):
    new_book: Book = kwargs["instance"]
    author, _ = Author.objects.get_or_create(name=new_book.author)
    author.books.add(new_book)


class Author(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.headline
