from django.db import transaction
from rest_framework.serializers import ModelSerializer

from .models import Tag


class TagsSerializer(ModelSerializer):
    """Serializer for `ManyToManyField` tags"""

    def to_internal_value(self, data):
        return super().to_internal_value({'title': data})

    def to_representation(self, instanse):
        return super().to_representation(instanse)['title']

    class Meta:
        model = Tag
        fields = ['title']


class SetTagsMixin:
    """Adds existing tags to instance when it is creating"""

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        instance = super().create(validated_data)

        for tag in tags:
            instance.tags.add(Tag.objects.get(title=tag['title']))

        instance.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        instance.tags.clear()

        for tag in tags:
            instance.tags.add(Tag.objects.get(title=tag['title']))

        instance.save()
        return instance