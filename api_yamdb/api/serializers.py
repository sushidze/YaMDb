from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User, ROLES


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(required=False, choices=ROLES)
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
        fields = '__all__'


class SignupSerializer(serializers.Serializer):
    regex = RegexValidator(
        '^[\w.@+-]+\Z$',
        'Letters, digits and @/./+/-/_ only.'
    )
    username = serializers.CharField(max_length=150, validators=[regex])
    email = serializers.EmailField(max_length=254)


class TokenSerializer(serializers.Serializer):
    regex = RegexValidator(
        '^[\w.@+-]+\Z$',
        'Letters, digits and @/./+/-/_ only.'
    )
    username = serializers.CharField(max_length=150,  validators=[regex])
    confirmation_code = serializers.CharField(max_length=10)
