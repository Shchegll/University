from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from api.views import PostViewSet, GroupViewSet, CommentViewSet


router = SimpleRouter()
router.register("posts", PostViewSet)
router.register("groups", GroupViewSet)
router.register(r"posts/(?P<post_id>\d+)/comments",
                CommentViewSet,
                basename="comments")

urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token),
    path("", include(router.urls)),
]
