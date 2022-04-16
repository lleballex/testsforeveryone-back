from django.db import transaction
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from ..models import Question, SolvedQuestion


class QuestionSerializer(ModelSerializer):
    """Serializer for receiving a question (when test solving)"""

    class Meta:
        model = Question
        fields = ['condition', 'image', 'kind', 'options']


class FullQuestionSerializer(ModelSerializer):
    """Serializer with all fields of a question"""

    class Meta:
        model = Question
        fields = ['id', 'condition', 'image', 'answer', 'options', 'kind']


class SolvedQuestionSerializer(ModelSerializer):
    """Serializer for question result of solved test"""

    is_right = SerializerMethodField()
    question = FullQuestionSerializer()

    class Meta:
        model = SolvedQuestion
        fields = ['is_right', 'user_answer', 'question']

    def get_is_right(self, obj):
        return obj.user_answer == obj.question.answer


class SetQuestionsMixin:
    """Creates and adds questions to the test when it is creating"""

    @transaction.atomic
    def create(self, validated_data):
        questions = validated_data.pop('questions', [])
        instance = super().create(validated_data)

        questions_serializer = FullQuestionSerializer(data=questions, many=True)            
        questions_serializer.is_valid(raise_exception=True)
        questions_serializer.save()

        for question in questions_serializer.data:
            instance.questions.add(Question.objects.get(id=question['id']))

        instance.save()
        return instance


