from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, ConfirmUser, CreateUser,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/auth/signup/', CreateUser.as_view(), name='signup'),
    path('v1/auth/token/', ConfirmUser.as_view(), name='get_token'),
    path('v1/', include(router_v1.urls)),
]
