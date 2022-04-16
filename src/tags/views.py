from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from .models import Tag
from .serializers import TagsSerializer


class TagsView(mixins.ListModelMixin, GenericAPIView):
    """Returns list of tags"""

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer

    def get(self, request):
        return self.list(request)