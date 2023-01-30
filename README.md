# YaMDb

This is an analogue of IMDb but about artworks where users rate, comment, write reviews and see current ratings. The YaMDb project collects user reviews of artworks. The works themselves are not stored in YaMDb, you cannot watch a movie or listen to music here.
Works are divided into categories and can be assigned to genre. 

Users have different roles (admin, moderator, user). Project backend implemented on Django using API. User registration implemented with POST-request and JWT-token response.

### Run

Clone repo and create venv:

```
git clone git@github.com:sushidze/api_yamdb.git
cd api_yamdb

python -m venv env
. venv/bin/activate
```

Install requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Do Django migrations and run project:

```
python manage.py migrate

python manage.py runserver
```

When project was successfully run you will see docs for API YaMDb following the link http://127.0.0.1:8000/redoc/

### Usage

You can add data to your db using csv-files. They should be located in /static/data/ with the following names:

users \
category \
genre \
titles \
genre_title \
review \
comments \

Import data:

```
python manage.py importcsv
```
