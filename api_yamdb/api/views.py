# from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from reviews.models import Category, Genre, Title
from .permissions import IsAdminUserOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSafeSerializer, TitleUnsafeSerializer)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для категорий.
    /categories/ - GET (anyone), POST (admin)
    /categories/{slug} - DELETE (admin)"""
    queryset = Category.objects.all()
    lookup_field = 'slug'  # we get categories/slug instea of ctgrs/pk mask
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для жанров.
    /genres/ - GET (anyone), POST (admin)
    /genres/{slug} - DELETE (admin)"""
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений.
    /genres/ - GET (anyone), POST (admin)
    /genres/{slug} - GET (anyone), DELETE (admin), PATCH (admin)"""
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSafeSerializer
        return TitleUnsafeSerializer
