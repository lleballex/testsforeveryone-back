from rest_framework.serializers import ModelSerializer

from .models import User
from tests.models import Test


class UserSerializer(ModelSerializer):
    """Serializer for user link"""

    class Meta:
        model = User
        fields = ['username', 'image']


class FullUserSerializer(ModelSerializer):
    """Serializer for receiving user (full data if it)"""

    class Meta:
        model = User
        fields = ['username', 'email', 'image']


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserTestsSerializer(ModelSerializer):
    """Serializer for receiving user tests"""

    class Meta:
        model = Test
        fields = ['id', 'title', 'image', 'rating']