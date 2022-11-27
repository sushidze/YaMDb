from django.urls import path, include
from rest_framework import routers

from api import views


v1_router = routers.DefaultRouter()
v1_router.register(r'categories', views.CategoryViewSet, basename='categories')
v1_router.register(r'genres', views.GenreViewSet, basename='genres')
v1_router.register(r'titles', views.TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
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
