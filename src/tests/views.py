from django.db import transaction
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .permissions import IsUnsolved, IsOwner
from core.rating.mixins import UpdateRatingMixin
from .models import Test, SolvedTest, SolvedQuestion
from .serializers import TestListSerializer, TestSerializer
from .serializers import OwnTestsSerializer, OwnTestSerializer
from .serializers import CreateTestSerializer, UpdateTestSerializer
from .serializers import SolvedTestsSerializer, SolvedTestSerializer

from datetime import datetime


class TestsView(mixins.ListModelMixin, mixins.CreateModelMixin,
                GenericAPIView):
    """Returns test list, creates new test"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TestListSerializer
        else:
            return CreateTestSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        sorting = self.request.query_params.get('sorting')
        tags = self.request.query_params.get('tags')

        tests = Test.objects.filter(is_available=True, title__contains=query)

        if tags:
            for tag in tags.split(','):
                tests = tests.filter(tags__title=tag)

        if sorting == 'old':
            tests = tests.order_by('date_created')

        return tests


class TestView(GenericAPIView):
    """Returns test (for solving) and solves test"""

    serializer_class = TestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Test.objects.all()
    lookup_field = 'id'

    def get(self, request, id):
        instance = self.get_object()
        data = self.get_serializer(instance).data

        if not request.user.is_authenticated:
            data.pop('questions')
            return Response({
                'status': 200,
                'test': data, 
            })

        if request.user.solved_tests.filter(test_id=instance.id):
            return Response({
                'status': 403,
                'detail': 'You have already solved this test',
                'solved_id': request.user.solved_tests.get(test_id=instance.id).id,
            })

        return Response({
            'status': 200,
            'test': data,
        })

    @transaction.atomic
    def post(self, request, id):
        test = self.get_object()

        date_started = datetime.fromtimestamp(request.data['start_date'] / 1000.0)
        date_ended = datetime.fromtimestamp(request.data['end_date'] / 1000.0)

        solved_test = SolvedTest.objects.create(test=test, user=request.user,
                                                date_started=date_started,
                                                date_ended=date_ended)

        for i in range(len(test.questions.all())):
            if test.questions.all()[i].answer == request.data['answers'][i]:
                solved_test.right_answers += 1

            solved_test.questions.add(SolvedQuestion.objects.create(
                user_answer=request.data['answers'][i],
                question=test.questions.all()[i],
            ))

        solved_test.save()

        return Response(solved_test.id, status=201)


class LikeTestView(UpdateRatingMixin, GenericAPIView):
    """Likes test"""

    queryset = Test.objects.all()
    lookup_field = 'id'

    def post(self, request, id):
        return self.like()


class DislikeTestView(UpdateRatingMixin, GenericAPIView):
    """Dislikes test"""

    queryset = Test.objects.all()
    lookup_field = 'id'

    def post(self, request, id):
        return self.dislike()


class OwnTestsView(mixins.ListModelMixin, GenericAPIView):
    """Returns own tests list"""

    serializer_class = OwnTestsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def get_queryset(self):
        return self.request.user.tests.all()


class OwnTestView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, GenericAPIView):
    """Returns information of own test and updates it"""

    queryset = Test.objects.all()
    permission_classes = [IsOwner]
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id)

    def post(self, request, id):
        return self.retrieve(request, id)

    def put(self, request, id):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request,id)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OwnTestSerializer
        return UpdateTestSerializer


class SolvedTestsView(mixins.ListModelMixin, GenericAPIView):
    """Returns solved tests list"""

    serializer_class = SolvedTestsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def get_queryset(self):
        return self.request.user.solved_tests.all()


class SolvedTestView(mixins.RetrieveModelMixin, GenericAPIView):
    """Returns results of solved test"""

    serializer_class = SolvedTestSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id)

    def get_queryset(self):
        return self.request.user.solved_tests.all()
