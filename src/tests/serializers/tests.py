from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from ..models import Test, SolvedTest
from users.serializers import UserSerializer
from core.serializers import ImageField, DateTimeField
from tags.serializers import TagsSerializer, SetTagsMixin
from .questions import QuestionSerializer, FullQuestionSerializer
from core.rating.serializers import IsLikedField, IsDislikedField
from .questions import SolvedQuestionSerializer, SetQuestionsMixin


TEST_FIELDS = ['title', 'user', 'image', 'tags', 'description', 'questions',
               'rating', 'is_liked', 'is_disliked', 'date_created']

def TEST_FIELDS_WITHOUT(*args):
    fields = TEST_FIELDS.copy()
    [fields.remove(arg) for arg in args]
    return fields


class TestSerializer(ModelSerializer):
    """Serializer for receiving a test (when test solving)"""

    user = UserSerializer(read_only=True)
    image = ImageField(required=False)
    tags = TagsSerializer(required=False, many=True)
    questions = QuestionSerializer(many=True)
    is_liked = IsLikedField()
    is_disliked = IsDislikedField()
    date_created = DateTimeField()

    class Meta:
        model = Test
        fields = TEST_FIELDS
        read_only_fields = ['rating', 'is_liked', 'is_disliked']


class TestListSerializer(TestSerializer):
    """Serializer for receiving a list of tests"""

    class Meta:
        model = Test
        fields = ['id'] + TEST_FIELDS_WITHOUT('questions', 'description')


class CreateTestSerializer(SetQuestionsMixin, SetTagsMixin, TestSerializer):
    """Serializer for creating a test"""

    questions = FullQuestionSerializer(many=True)


class UpdateTestSerializer(SetTagsMixin, TestSerializer):
    """Serializer for updating a test"""

    class Meta:
        model = Test
        fields = TEST_FIELDS_WITHOUT('questions')
        read_only_fields = ['rating', 'is_liked', 'is_disliked']


class TestSolutionSerializer(ModelSerializer):
    """Serializer for receiving somebody solutions of own test"""

    user = UserSerializer()
    questions = SolvedQuestionSerializer(many=True)
    date_started = DateTimeField()
    date_ended = DateTimeField()

    class Meta:
        model = SolvedTest
        fields = ['user', 'questions', 'right_answers', 'date_started', 'date_ended']


class OwnTestsSerializer(TestSerializer):
    """Serializer for receiving a list of own tests"""

    solutions = SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'solutions'] + TEST_FIELDS_WITHOUT('user', 'description',
                                                           'is_liked', 'is_disliked',
                                                           'questions')

    def get_solutions(self, obj):
        return obj.solutions.count()


class OwnTestSerializer(TestSerializer):
    """Serializer for receiving information and solutions of own test"""

    questions = FullQuestionSerializer(many=True)
    solutions = TestSolutionSerializer(many=True)

    class Meta:
        model = Test
        fields = TEST_FIELDS + ['solutions']









class SolvedTestsSerializer(ModelSerializer):
    """Serializer for receiving list of solved tests"""

    title = SerializerMethodField()
    image = SerializerMethodField()
    tags = SerializerMethodField()
    questions = SerializerMethodField()
    date_ended = DateTimeField()

    class Meta:
        model = SolvedTest
        fields = ['id', 'title', 'image', 'tags', 'questions',
                  'right_answers', 'date_ended']

    def get_title(self, obj):
        return obj.test.title

    def get_image(self, obj):
        return obj.test.image.url if obj.test.image else None

    def get_tags(self, obj):
        return TagsSerializer(obj.test.tags.all(), many=True).data

    def get_questions(self, obj):
        return obj.questions.count()


class s(TestSerializer):
    class Meta:
        model = Test
        fields = ['id'] + TEST_FIELDS_WITHOUT('questions')


class SolvedTestSerializer(ModelSerializer):
    """Serializer for receiving results of solved test"""

    test = s()
    questions = SolvedQuestionSerializer(many=True)
    date_started = DateTimeField()
    date_ended = DateTimeField()

    class Meta:
        model = SolvedTest
        fields = ['test', 'questions', 'date_started', 'date_ended']