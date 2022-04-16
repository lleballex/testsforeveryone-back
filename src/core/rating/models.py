from django.db import models

from users.models import User


class ModelWithRating(models.Model):
    """Base class that adds rating fields to model"""

    rating = models.IntegerField(default=0)
    liked_users = models.ManyToManyField(User, blank=True, related_name='liked_%(class)ss')
    disliked_users = models.ManyToManyField(User, blank=True, related_name='dislikeds_%(class)ss')

    class Meta:
        abstract = True