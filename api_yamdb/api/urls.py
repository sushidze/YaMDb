from django.urls import path, include
from rest_framework import routers

from api.views import (MyViewSet, signup, token, CategoryViewSet,
                       GenreViewSet, TitleViewSet, ReviewViewSet,
                       CommentViewSet)

v1_router = routers.DefaultRouter()
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token, name='token'),
    path(
        'users/me/',
        MyViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
        name='signup'
    ),
    path('', include(v1_router.urls)),
]
