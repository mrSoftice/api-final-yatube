from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import (
    CommentViewSet,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    FollowViewSet,
    GroupViewSet,
    PostViewSet,
)

router_v1 = DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='posts')
router_v1.register(r'groups', GroupViewSet, basename='groups')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    'comments'
)
router_v1.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path(
        "v1/jwt/create/",
        TokenObtainPairView.as_view(),
        name="jwt-create"
    ),
    path(
        "v1/jwt/refresh/",
        CustomTokenRefreshView.as_view(),
        name="jwt-refresh"
    ),
    path(
        "v1/jwt/verify/",
        CustomTokenVerifyView.as_view(),
        name="jwt-verify"
    ),
    path('v1/', include(router_v1.urls)),
]
