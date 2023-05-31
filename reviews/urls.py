from rest_framework import routers

from .views import CommentViewSet, RatingViewSet, FavouriteViewSet

router = routers.DefaultRouter()
router.register('comment', CommentViewSet, basename='comment')
router.register('rating', RatingViewSet, basename='rating')
router.register('favourite', FavouriteViewSet, basename='favourite')

urlpatterns = router.urls