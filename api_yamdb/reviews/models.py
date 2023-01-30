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
        verbose_name='name'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='identifier'
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """The genres class is used to store data about the genres of a work."""

    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='name'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='identifier'
    )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """The class of the artwork. Stores the titles of the artworks."""

    STR_PRESENTATION = ('{category} "{name}" ({year}) -'
                        '{rating}/10: {description:.16}')
    name = models.CharField(max_length=256, verbose_name='name')
    year = models.IntegerField(
        validators=(MinValueValidator(-3000), MaxValueValidator(2050)),
        verbose_name='publication year'
    )
    rating = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        blank=True,
        null=True,
        verbose_name='rating'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='description'
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
        verbose_name = 'Artworks'
        verbose_name_plural = 'Artworks'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'year'),
                name='unique_follow_relation'
            ),
        )

    def update_rating(self):
        """A function to update the rating for calling when working with reviews."""
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
        verbose_name='artwork'
    )
    text = models.TextField(
        verbose_name='review text',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='review author'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Choose value from 1 to 10'),
            MaxValueValidator(10, message='Ser value from 1 to 10')
        ],
        verbose_name='score'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date of review'
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
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
        verbose_name='review'
    )
    text = models.TextField(
        verbose_name='comment text',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='comment author'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='comment date'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        default_related_name = 'comments'
        ordering = ['pub_date']
