from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    """Класс медиумов.
    Поля: name: str, slug: str."""
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

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Класс жанров. (Одно произведение - любое количество жанров.)
    Поля: name: str, slug: str."""
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

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Класс произведения.
    Поля: name: str, year: int [-3000; 2050], rating: int [1; 10],
    description: str, category: Category (many-to-one),
    genres: Genre (many-to-many)."""
    STR_PRESENTATION = ('{category} "{name}" ({year}) -'
                        '{rating}/10: {description:.16}')
    name = models.CharField(max_length=256, verbose_name='название')
    year = models.IntegerField(
        validators=(MinValueValidator(-3000), MaxValueValidator(2050)),
        verbose_name='год публикации'
    )
    rating = models.PositiveIntegerField(
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
    # пожалуй, в прокси-модели нет необходимости

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'year'),
                name='unique_follow_relation'
            ),
        )
        # могут быть тайтлы с одинаковым названием,
        # но при условии, что они вышли в разное время

    def __str__(self):
        return self.STR_PRESENTATION.format(
            category=self.category.name,
            name=self.name,
            rating=self.rating,
            description=self.description
        )
