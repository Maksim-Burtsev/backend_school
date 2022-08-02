# Яндекс.Товары

## *Вступительное задание в летнюю школу backend-разработки Yandex* ##

Примеры ответов, описание «ручек» и предварительные тесты находятся в папке [«Technical Task»](https://github.com/Maksim-Burtsev/backend_school/tree/master/Technical%20Task).

Описание задания находится там же, [ссылка на него](https://github.com/Maksim-Burtsev/backend_school/blob/master/Technical%20Task/Task.md).

### **В проекте используются:**

- Django
- <a href="https://github.com/vitalik/django-ninja">django-ninja</a>
- <a href='https://github.com/django-mptt/django-mptt'>django-mptt</a>
- Postgres
- Docker
- unittest

### **Auto Swagger Docs**

В проекте есть документация API, которая доступна по ссылке **'/docs'**

<img src='docs.jpg'>

## **Запуск проекта**

    docker-compose up --build

## **Запусков тестов**

    docker-compose  run --rm  web python manage.py test

    или

    make test
