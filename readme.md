## what is this:

This is django, djangorestframework related task 4 starlab.

## what i've done:

- decided to use `Django` and `DRF` for this task
- created `Book` and `Author` models, with `many-to-many` realation.
- writted tests on all `CRUD` endpoints, `./books/tests.py`
- there is validations of necessary field in the `POST` of `Book`.
- project is working with `sqlite.db`
- you can upload book files through the django `admin`

## how to run it:

Create venv using whatever method you want, example:
```bash
mkvirtualenv starlab-task
```

Activate it:
```bash
workon starlab-task
```

Install some dependencies:
```bash
pip install -r requirements.txt
```

Apply some migrations:
```bash
python manage.py migrate
```

Create some superusers:
```bash
python manage.py createsuperuser
```

Go check some admin of this app (go to `/admin`)

Run the project:
```bash
python manage.py runserver
```

Now, you can go to `/admin`, there will be 2 Books and 1 Author, created
in the migration file, you can add some book_files using admin, then go
to `/books` endpoint and test if you can download book files using links.


## how to run tests:

```
python manage.py test
```