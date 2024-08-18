# контейнер будет работать на python alpine image
FROM python:alpine

# Меняем рабочую директорию в контейнере
WORKDIR /app

# Копируем весь код из папки проекта в директории в контейнере
ADD . /app

# Устанавливаем зависимости
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

# Делаем 8000 порт контейнера доступным
EXPOSE 8000

# Запускаем проект в контейнере
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]