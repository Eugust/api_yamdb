from django.urls import include, path
from rest_framework.routers import DefaultRouter
from reviews.views import CategoryViewSet, GenreViewSet, TitleViewSet
from users.views import UserViewSet, get_jwt_token, send_confirmation_code

from .views import CommentViewSet, ReviewViewSet

v1_router = DefaultRouter()
v1_router.register(
    'users',
    UserViewSet,
    basename='users'
)
v1_router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
v1_router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

v1_auth_patterns = [
    path('signup/', send_confirmation_code, name='register_user'),
    path('token/', get_jwt_token, name='generate_token'),
]

urlpatterns = [
    path('v1/auth/', include(v1_auth_patterns)),
    path('v1/', include(v1_router.urls)),
]
