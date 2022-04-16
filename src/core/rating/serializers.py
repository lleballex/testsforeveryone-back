from rest_framework.serializers import SerializerMethodField


class IsLikedField(SerializerMethodField):
    def to_representation(self, instance):
        return bool(instance.liked_users.filter(id=self.context['request'].user.id))


class IsDislikedField(SerializerMethodField):
    def to_representation(self, instance):
        return bool(instance.disliked_users.filter(id=self.context['request'].user.id))