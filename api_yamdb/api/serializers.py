import datetime as dt
from rest_framework import serializers
from rest_framework.validators import ValidationError

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для категорий.
    Параметр пути - слаг."""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для жанров.
    Параметр пути - слаг."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSafeSerializer(serializers.ModelSerializer):
    """Сериалайзер для произведений при запросах list | retrieve.
    Сериализаторы категорий и жанра вложены."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleUnsafeSerializer(serializers.ModelSerializer):
    """Сериалайзер для произведений при небезопасных запросах."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise ValidationError(f'{value} год еще не настал')
        return value

    def validate(self, data):
        if Title.objects.filter(
            name=data['name'],
            year=data['year']
        ).exists():
            raise ValidationError('Такой тайтл уже есть')
        return data
