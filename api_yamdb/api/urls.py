from django.urls import include, path
from rest_framework import routers

from api import views

v1_router = routers.DefaultRouter()
v1_router.register(r'categories', views.CategoryViewSet, basename='categories')
v1_router.register(r'genres', views.GenreViewSet, basename='genres')
v1_router.register(r'titles', views.TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # path('', include('djoser.urls.jwt')),
]
