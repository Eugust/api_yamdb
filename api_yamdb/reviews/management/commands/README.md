### Проект YaMDb. Когорта 17. Спринт 11. Teamwork 3.6
-----------------------------------------------------
## Описание команды import_csv
Команда нужна для автоматической пакетной загрузки
данных из CSV файлов (папка ./static/data/*.csv).

Заливка данных осуществляется в пустую базу.
Перед выполнением скрипта нужно применить миграции

```
python3 ./api_yamdb/manage.py migrate
python3 ./api_yamdb/manage.py makemigrations
```

### Команда
```
python ./api_yamdb/manage.py import_csv 
```

### Работа скрипта
- Просканировать папки и получить список файлов
- Загрузить данные из файлов.
  Последовательность наполнения
моделей задается строками 103-109
```
self.handle_file('users')
self.handle_file('category')
self.handle_file('genre')
self.handle_file('titles')
self.handle_file('review')
self.handle_file('comments')
self.handle_connections('genre_title')
```
- Список имен файлов и его связь с моделями указаны
в строках 12-20
```
PAIRS = {
    'users': ['User', 'users', 'filepath'],
    'genre': ['Genre', 'reviews', 'filepath'],
    'titles': ['Title', 'reviews', 'filepath'],
    'comments': ['Comment', 'reviews', 'filepath'],
    'review': ['Review', 'reviews', 'filepath'],
    'category': ['Category', 'reviews', 'filepath'],
    'genre_title': ['Title', 'reviews', 'filepath']
}
```
Формат – "Имя файла": [Модель, приложение, путь к файлу]

Путь к файлу записывается при старте скрипта.
