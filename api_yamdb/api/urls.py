from django.urls import path, include

from api.views import MyViewSet, signup, token

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token, name='token'),
    path(
        'users/me/',
        MyViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
        name='signup'
    ),
]
