from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .serializers import ArticleSerializer
from .models import Article, Tag
from permissions.permissions import IsAuthor


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filterset_fields = ['tag__title', 'status']
    search_fields = ['title', 'text']
    

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthor]

        return super().get_permissions()
    
    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context['TEST_KEY'] = 'TEST EPTA'
        return context
    
    
