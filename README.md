Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:sushidze/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Когда вы запустите проект, для API YaMDb будет доступна документация по адресу:

```
http://127.0.0.1:8000/redoc/
```

Можно заполнить базу из набора csv-файлов. Они должны лежать в /static/data/ и иметь названия:

users
category
genre
titles
genre_title
review
comments

Для импорта запустите команду:

```
python manage.py importcsv
```