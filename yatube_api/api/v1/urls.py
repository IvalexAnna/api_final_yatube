from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, FollowViewSet, GroupViewSet, CommentViewSet

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("follow", FollowViewSet, basename='follow')
router.register("groups", GroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "posts/<int:post_pk>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="post-comments",
    ),
    path(
        "posts/<int:post_pk>/comments/<int:pk>/",
        CommentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="comment-detail",
    ),
    path("jwt/", include("api.v1.jwt_urls")),
]
