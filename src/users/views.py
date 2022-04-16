from rest_framework import mixins
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ParseError, PermissionDenied

from .models import User
from .utils import encode_auth_token
from .serializers import UserSerializer, CreateUserSerializer
from .serializers import UserTestsSerializer, FullUserSerializer


class SignInView(APIView):
    """Returns user data after user is signed in"""

    def get(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        else:
            raise PermissionDenied()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            raise ParseError('Request must have username field')
        if not password:
            raise ParseError('Request must have password field')

        user = authenticate(username=username, password=password)

        if not user:
            raise ParseError('Username or password is invalid')

        return Response({
            'token': encode_auth_token(user.id),
            'user': UserSerializer(user).data,
        })


class SignUpView(mixins.CreateModelMixin, GenericAPIView):
    """Registers new user"""

    serializer_class = CreateUserSerializer

    def post(self, request):
        return self.create(request)


class UserView(GenericAPIView):
    """Returns user (for user page)"""

    queryset = User.objects.all()
    lookup_field = 'username'

    def overview(self, instance):
        tests = instance.tests.order_by('-rating', '-date_created')[:6]
        return Response({
            'tests': UserTestsSerializer(tests, many=True,
                                            context={'request': self.request}).data,
        })

    def tests(self, instance):
        tests = instance.tests.all()
        return Response({
            'tests': UserTestsSerializer(tests, many=True,
                                         context={'request': self.request}).data
        })

    def get(self, request, username):
        area = request.query_params.get('area')
        instance = self.get_object()

        if area == 'tests':
            response = self.tests(instance)
        else:
            response = self.overview(instance)

        response.data.update(user=FullUserSerializer(instance).data)
        return response