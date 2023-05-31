from rest_framework import routers

from .views import ArticleViewSet

router = routers.DefaultRouter()
router.register('article', ArticleViewSet, basename='article')

urlpatterns = router.urls