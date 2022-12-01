from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from api.filters import FilterForTitles
from api.permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                             IsAdminUserOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, SafeTitleSerializer,
                             ReviewSerializer, SignupSerializer,
                             TitleSerializer, TokenSerializer,
                             UserEditSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="YaMDb registration",
        message=f"Your confirmation code: {confirmation_code}",
        from_email=None,
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )

    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)

    def perform_destroy(self, review):
        review.delete()
        review.title.update_rating()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id")
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)


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
    queryset = Title.objects.all().annotate(Avg("reviews__score"))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filterset_class = FilterForTitles
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return SafeTitleSerializer
        return TitleSerializer
