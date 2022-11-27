import random

from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import ForMeOnly, AdminOnly
from api.serializers import UserSerializer, SignupSerializer, TokenSerializer
from reviews.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    search_fields = ('username',)
    lookup_field = 'username'


class MyViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (ForMeOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        if request.data.get('role'):
            dict_to_operate = dict()
            for key, value in request.data.items():
                dict_to_operate[key] = value
            dict_to_operate.pop('role')
            serializer = self.get_serializer(
                instance,
                data=dict_to_operate,
                partial=True
            )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        if username == 'me':
            return Response(
                'Это имя недоступно',
                status=status.HTTP_400_BAD_REQUEST
            )
        email = serializer.data.get('email')
        confirmation_code = str(random.randint(100000, 999999))
        send_mail(
            'Код потверджения регистрации в YamDB',
            f'Ваш код подтверждения: {confirmation_code}',
            '21team@praktikum.ru',
            [email, ],
            fail_silently=False,
        )
        if User.objects.filter(username=username).exists():
            found_user = User.objects.get(username=username)
            found_user.confirmation_code = confirmation_code
            found_user.save()
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            found_user = User.objects.get(email=email)
            found_user.confirmation_code = confirmation_code
            found_user.save()
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST
            )
        User.objects.create_user(
            username=username,
            email=email,
            confirmation_code=confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        if User.objects.filter(username=username).exists():
            current_user = User.objects.get(username=username)
            if str(current_user.confirmation_code) != confirmation_code:
                return Response(
                    'Неверный код подтверждения',
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = str(RefreshToken.for_user(current_user).access_token)
            current_user.confirmation_code = None
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response(
                'Пользователь не найден',
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
