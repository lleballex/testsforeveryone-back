from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def update_rating(user, instance, current, other):
    if current.filter(id=user.id):
        current.remove(user)
        user_exists = False
    else:
        current.add(user)
        user_exists = True

    if other.filter(id=user.id):
        other.remove(user)

    instance.rating = instance.liked_users.count() - instance.disliked_users.count()
    instance.save()

    return (instance.rating, user_exists)



class UpdateRatingMixin:
    """Increases and decreases rating"""

    permission_classes = [IsAuthenticated]

    def like(self):
        instance = self.get_object()
        result = update_rating(self.request.user, instance,
                               instance.liked_users, instance.disliked_users)
        return Response({
            'rating': result[0],
            'is_liked': result[1]
        })

    def dislike(self):
        instance = self.get_object()
        result = update_rating(self.request.user, instance,
                               instance.disliked_users, instance.liked_users)

        return Response({
            'rating': result[0],
            'is_disliked': result[1],
        })