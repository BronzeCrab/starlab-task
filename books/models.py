from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=30)
    date_published = models.DateField(auto_now_add=True)
    genre = models.CharField(max_length=30)
    book_file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name
