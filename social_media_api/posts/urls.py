from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentListCreateView, CommentRetrieveUpdateDestroyView
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentListCreateView, CommentRetrieveUpdateDestroyView, UserFeedView
from .views import FeedView

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentListCreateView, CommentRetrieveUpdateDestroyView, UserFeedView, LikePostView # Import LikePostView

from django.urls import path
from .views import LikePostView





router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet)






urlpatterns = [
    path('', include(router.urls)),
    path('feed/', UserFeedView.as_view(), name='user_feed'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('posts/<int:post_id>/comments/<int:comment_id>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like_post'), # New like path
    path('posts/<int:pk>/unlike/', LikePostView.as_view(), name='unlike_post'), # New unlike path (using the same view)
]

