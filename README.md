# Вступительное задание в летнюю школу backend-разработки #

## В проекте используются:

- Django
- <a href="https://github.com/vitalik/django-ninja">django-ninja</a>
- Postgres
- Docker
- unittest

## Auto Swagger Docs
В проекте есть документация API, которая доступна по ссылке **'/docs'**  

<img src='docs.jpg'>

## Запуск проекта

    docker-compose up --build

    или

    make run

## Запусков тестов

    docker-compose  run --rm  web python manage.py test

    или 

    make test


