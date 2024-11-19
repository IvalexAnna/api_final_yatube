from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"follow", FollowViewSet)
router.register(r"groups", GroupViewSet)

# Вложенные маршруты для комментариев
urlpatterns = [
    path("", include(router.urls)),
    path(
        "posts/<int:post_pk>/",
        include(
            (
                [
                    path(
                        "comments/",
                        CommentViewSet.as_view({"get": "list", "post": "create"}),
                        name="post-comments",
                    ),
                    path(
                        "comments/<int:id>/",
                        CommentViewSet.as_view(
                            {
                                "get": "retrieve",
                                "put": "update",
                                "patch": "partial_update",
                                "delete": "destroy",
                            }
                        ),
                        name="comment-detail",
                    ),
                ],
                "comments",
            )
        ),
    ),
]
