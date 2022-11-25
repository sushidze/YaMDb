from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError

from reviews.models import Comment, Review, Title


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


class CommentSeializer(serializers.ModelSerializer):
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
