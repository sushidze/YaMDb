import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Title, User

from api_yamdb.settings import STATICFILES_DIRS

DATA_DIR = f'{STATICFILES_DIRS[0]}/data/'


def parse_users(path):
    """id,username,email,role,bio,first_name,last_name"""
    users = []
    with open(path) as file:
        next(file)  # пропускаем 1ую строку в файле (шапку таблицы)
        reader = csv.reader(file)
        for row in reader:
            users.append(User(
                pk=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            ))
    User.objects.bulk_create(users)


def parse_categories(path):
    """id,name,slug"""
    categories = []
    with open(path) as file:
        next(file)  # пропускаем 1ую строку в файле (шапку таблицы)
        reader = csv.reader(file)
        for row in reader:
            categories.append(Category(
                pk=row[0],
                name=row[1],
                slug=row[2],
            ))
    Category.objects.bulk_create(categories)


def parse_genres(path):
    """id,name,slug"""
    genres = []
    with open(path) as file:
        next(file)  # пропускаем 1ую строку в файле (шапку таблицы)
        reader = csv.reader(file)
        for row in reader:
            genres.append(Genre(
                pk=row[0],
                name=row[1],
                slug=row[2],
            ))
    Genre.objects.bulk_create(genres)


def parse_titles(path):
    """id,name,year,category"""
    titles = []
    with open(path, encoding="utf-8") as file:
        next(file)  # пропускаем 1ую строку в файле (шапку таблицы)
        reader = csv.reader(file)
        for row in reader:
            titles.append(Title(
                pk=row[0],
                name=row[1],
                year=row[2],
                category=Category.objects.get(pk=row[3])
            ))
    Title.objects.bulk_create(titles)


def set_genre_title_relations(path):
    """id(unused),title_id,genre_id"""
    with open(path) as file:
        next(file)  # пропускаем 1ую строку в файле (шапку таблицы)
        reader = csv.reader(file)
        for row in reader:
            Title.objects.get(pk=row[1]).genre.add(
                Genre.objects.get(pk=row[2])
            )


def parse_reviews(path):
    """id,title_id,text,author,score,pub_date"""
    reviews = []
    titles = set()
    with open(path, encoding="utf-8") as file:
        next(file)  # пропускаем 1ую строку в файле (шапку таблицы)
        reader = csv.reader(file)
        for row in reader:
            title = Title.objects.get(pk=row[1])
            reviews.append(Review(
                pk=row[0],
                title=title,
                text=row[2],
                author=User.objects.get(pk=row[3]),
                score=row[4],
                pub_date=row[5]
            ))
            titles.add(title)
    Review.objects.bulk_create(reviews)
    for title in titles:
        title.update_rating()


def parse_comments(path):
    """id,review_id,text,author,pub_date"""
    comments = []
    with open(path, encoding="utf-8") as file:
        next(file)  # пропускаем 1ую строку в файле (шапку таблицы)
        reader = csv.reader(file)
        for row in reader:
            comments.append(Comment(
                pk=row[0],
                review=Review.objects.get(pk=row[1]),
                text=row[2],
                author=User.objects.get(pk=row[3]),
                pub_date=row[4]
            ))
    Comment.objects.bulk_create(comments)


class Command(BaseCommand):
    help = 'Parses csv files to fill a base'

    def handle(self, *args, **options):
        # [callable, file name]
        parse_cases = [
            [parse_users, 'users'],
            [parse_categories, 'category'],
            [parse_genres, 'genre'],
            [parse_titles, 'titles'],
            [set_genre_title_relations, 'genre_title'],
            [parse_reviews, 'review'],
            [parse_comments, 'comments'],
        ]
        errors = []
        for func, file in parse_cases:
            try:
                func(f'{DATA_DIR}{file}.csv')
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully parsed {file}')
                )
            except Exception as error:
                errors.append((file, error))
            if errors:
                raise CommandError(f'Cannot parse {errors}')
