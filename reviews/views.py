from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from .models import Comment, Favourite, Rating
from .serializers import CommentSerializer, FavouriteSerializer, RatingSerializer
from permissions.permissions import IsAuthor

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]

        elif self.request.method in ['DELETE', 'PATCH', 'PUT']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()

class FavouriteViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)
    serializer_class = FavouriteSerializer





class RatingViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        
        else:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()


