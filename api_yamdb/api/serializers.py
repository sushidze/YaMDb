from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
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
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User
        read_only_fields = ('role',)


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Username "me" is not valid')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


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
        title_id = self.context['view'].kwargs.get('title_id')
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                title=get_object_or_404(Title, pk=title_id),
                author=self.context['request'].user
            ).exists():
                raise ValidationError(
                    'Отзыв к данному произведению уже добавлен'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


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
        fields = '__all__'


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


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class SafeTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
