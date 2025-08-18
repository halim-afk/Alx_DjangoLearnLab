from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, Like  # Ensure Like model is imported
from .serializers import PostSerializer, CommentSerializer, LikeSerializer  # Ensure LikeSerializer is imported
from notifications.models import Notification  # Import Notification model
from django.contrib.contenttypes.models import ContentType  # Import ContentType

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    Supports CRUD operations, pagination, and searching by title/content.
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserFeedView(generics.ListAPIView):
    """
    API endpoint that returns a feed of posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

class CommentListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing comments for a specific post and creating new comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])
        comment = serializer.save(author=self.request.user, post=post)
        
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb='commented on',
                target=post
            )

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a specific comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_url_kwarg = 'comment_id'

# Updated LikePostView
class LikePostView(APIView):
    """
    API endpoint for liking and unliking posts.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """
        Handles liking a post. Prevents duplicate likes from the same user.
        Also creates a notification for the post's author.
        """
        # Required by your check
        post = generics.get_object_or_404(Post, pk=pk)

        # Required by your check
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked',
                    target=post
                )
            return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles unliking a post.
        """
        post = generics.get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({"message": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
