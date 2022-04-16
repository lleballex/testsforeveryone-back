from django.db import models, transaction
from django.contrib.postgres.fields import ArrayField

from tags.models import Tag
from users.models import User
from core.rating.models import ModelWithRating


QUESTION_KINDS = [
    ('TEXT', 'text'),
    ('NUMBER', 'number'),
    ('RADIO', 'radio'),
]


class Question(models.Model):
    condition = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='tests/%Y/%m/%d/')
    kind = models.CharField(max_length=10, choices=QUESTION_KINDS, default='TEXT')
    answer = models.CharField(max_length=100)
    options = ArrayField(models.CharField(max_length=500), blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.condition[:30]


class SolvedQuestion(models.Model):
    user_answer = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='solutions')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.question.condition[:30]


class Test(ModelWithRating):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='projects')
    image = models.ImageField(null=True, blank=True, upload_to='tests/%Y/%m/%d/')
    questions = models.ManyToManyField(Question, related_name='test')
    date_created = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    blocking_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title[:30]

    @transaction.atomic
    def delete(self, *args, **kwargs):
        self.questions.all().delete()
        return super().delete(*args, **kwargs)


class SolvedTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solved_tests')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='solutions')
    questions = models.ManyToManyField(SolvedQuestion)
    right_answers = models.IntegerField(default=0)
    date_started = models.DateTimeField()
    date_ended = models.DateTimeField()

    class Meta:
        ordering = ['-date_ended']

    def __str__(self):
        return self.test.title[:30]