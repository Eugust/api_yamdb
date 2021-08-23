### Проект YaMDb. Когорта 17. Спринт 11. Teamwork 3.6
-----------------------------------------------------
## Описание
Проект YaMDb собирает отзывы пользователей на произведения
различных категорий и жанров

### Технологии
- django==2.2.16
- djangorestframework==3.12.4
- djangorestframework-simplejwt==4.7.2
- django-filter==2.4.0
- requests
- pytest


### Запуск проекта в dev-режиме
- Клонировать репозиторий.
- Создать и активировать виртуальное окружение.
- Обновить pip:
```
python3 -m pip install --upgrade pip
``` 
- Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
``` 
- Выполнить миграции:
```
python3 manage.py migrate
python3 manage.py makemigrations
``` 
- Импортировать тестовые данные:
```
python ./api_yamdb/manage.py import_csv 
```
- Запустить проект:
```
python3 manage.py runserver
```
## Примеры API запросов
См. [Страница Redoc](http://127.0.0.1:8000/redoc/)

### Авторы
- Илюшин Григорий
- Устинов Евгений
- Черных Василий

--------------------------------------------
### api_yamdb
Feel free to contact us
