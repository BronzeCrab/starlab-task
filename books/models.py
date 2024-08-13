from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.headline