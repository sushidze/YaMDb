from statistics import mean

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    ]

    bio = models.CharField(max_length=250, null=True, blank=True)
    role = models.CharField(max_length=20, default='user', choices=ROLES)
    confirmation_code = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='название'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='идентификатор'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Класс жанры служит для хранения данных о жанрах произведения."""

    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='название'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='идентификатор'
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Класс произведения. Хранит в себе названия произведений."""

    STR_PRESENTATION = ('{category} "{name}" ({year}) -'
                        '{rating}/10: {description:.16}')
    name = models.CharField(max_length=256, verbose_name='название')
    year = models.IntegerField(
        validators=(MinValueValidator(-3000), MaxValueValidator(2050)),
        verbose_name='год публикации'
    )
    rating = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        blank=True,
        null=True,
        verbose_name='рейтинг'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='описание'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'year'),
                name='unique_follow_relation'
            ),
        )

    def update_rating(self):
        """Функция для обновления рейтинга для вызова при работе с отзыами."""
        self.rating = round(mean(
            [review.score for review in self.reviews.all()]
        ))
        self.save()

    def __str__(self):
        return self.STR_PRESENTATION.format(
            category=self.category.name,
            name=self.name,
            rating=self.rating,
            description=self.description
        )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Укажите число от 1 до 10'),
            MaxValueValidator(10, message='Укажите число от 1 до 10')
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ['pub_date']
