# Generated by Django 5.1 on 2024-08-18 13:45

from django.db import migrations, models
from django.contrib.auth.models import User

from datetime import datetime


def forwards_func(apps, schema_editor):
    Book = apps.get_model("books", "Book")
    Author = apps.get_model("books", "Author")
    db_alias = schema_editor.connection.alias
    b1 = Book(
        title="book_1", genre="test_genre_1", date_published=datetime.now().date()
    )
    b2 = Book(
        title="book_2", genre="test_genre_2", date_published=datetime.now().date()
    )
    b3 = Book(title="Dune", genre="test_genre_3", date_published=datetime.now().date())
    Book.objects.using(db_alias).bulk_create([b1, b2, b3])
    a1 = Author(name="Author1")
    a1.save()
    a1.books.add(b1, b2)
    a2 = Author(name="Frank Herbert")
    a2.save()
    a2.books.add(b3)

    user = User.objects.create(username="user_0", is_staff=True)
    user.set_password("user_0")
    user.save()


def reverse_func(apps, schema_editor):
    Book = apps.get_model("books", "Book")
    Author = apps.get_model("books", "Author")
    db_alias = schema_editor.connection.alias
    Book.objects.using(db_alias).filter(title="book_1", genre="test_genre_1").delete()
    Book.objects.using(db_alias).filter(title="book_2", genre="test_genre_2").delete()
    Author.objects.using(db_alias).filter(name="Author1").delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=30)),
                ("date_published", models.DateField()),
                ("genre", models.CharField(max_length=30)),
                ("book_file", models.FileField(upload_to="")),
                ("is_denied", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("books", models.ManyToManyField(to="books.book")),
            ],
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
