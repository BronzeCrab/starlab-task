## what is this:

This is django, djangorestframework related task 4 starlab

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

## how to run tests:

```bash
python manage.py test
```