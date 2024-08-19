## what is this:

This is django, djangorestframework related task 4 starlab.

## what i've done:

- decided to use `Django` and `DRF` for this task.
- created `Book` and `Author` models, with `many-to-many` realation.
- writted tests on all `CRUD` endpoints, `./books/tests.py`.
- there is validations of necessary field in the `POST` of `Book`.
- project is working with `sqlite.db`.
- you can upload book files through the django `admin`.
- added some testing scripts, in the `testing_scripts` folder. First script (`denied_xlsx_test.py`)
  if for testing of `denied` file upload. Second script (`create_new_book_with_file_test.py`) is
  for testing `Book` creation with file.
- implemented `FileUploadView` endpoint which can receive `files`,
  parse it and find specific `Book`s  in the `db` and set `is_denied` to `True`.
- I set up the `django` loggin (all logs are saved to `general.log` in the `root` of project).
- Added `Dockerfile`.
- No view of `Book` files, sorry, only download.
- You can check creating of the `Book` and setting `book_file` using `create_new_book_with_file_test.py` script.

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

Now, you can go to `/admin`, there will be 2 `Books` and 1 `Author`, created
in the migration file - `0001_initial.py`, you can add some book files using `admin`, then go
to `/books` endpoint and test if you can download book files using given links.


## How to run project using `Docker`:

```sh
sudo docker build -t starlabtask .
```

Then:

```sh
sudo docker run -p 4000:8000 starlabtask
```

then

```sh
sudo docker exec -it starlabtask sh -c "python manage.py migrate"
```

then

```sh
sudo docker exec -it starlabtask sh -c "python manage.py createsuperuser"
```


## how to run testing scripts:

You cand run testin scripts from the root of the project, for example,
to test `FileUploadView` endpoint (parsing `decline_list`):

```sh
python testing_scripts/denied_xlsx_test.py
```

## how to run tests:

```
python manage.py test
```