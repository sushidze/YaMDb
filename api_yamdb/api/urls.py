from django.urls import include, path
from rest_framework import routers

from api import views

v1_router = routers.DefaultRouter()
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
    path('v1/', include(v1_router.urls)),
]
