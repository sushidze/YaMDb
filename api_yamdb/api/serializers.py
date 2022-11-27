import datetime as dt
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Category, Genre, Review, Title
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError

from reviews.models import User, ROLES


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(required=False, choices=ROLES)
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = '__all__'


class SignupSerializer(serializers.Serializer):
    regex = RegexValidator(
        '^[\w.@+-]+\Z$',
        'Letters, digits and @/./+/-/_ only.'
    )
    username = serializers.CharField(max_length=150, validators=[regex])
    email = serializers.EmailField(max_length=254)


class TokenSerializer(serializers.Serializer):
    regex = RegexValidator(
        '^[\w.@+-]+\Z$',
        'Letters, digits and @/./+/-/_ only.'
    )
    username = serializers.CharField(max_length=150,  validators=[regex])
    confirmation_code = serializers.CharField(max_length=10)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Отзыв к данному произведению уже добавлен'
                )
        return data

    class Meta:
        model = Review
        fields = ('__all__')


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('__all__')


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
