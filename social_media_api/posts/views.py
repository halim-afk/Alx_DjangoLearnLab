from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from notifications.models import Notification # Import Notification model
from django.contrib.contenttypes.models import ContentType # Import ContentType
from django.db import IntegrityError # Import IntegrityError
try:
    # Try to create a like
    Like.objects.create(user=request.user, post=post)
    # ... create notification ...
    return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)
except IntegrityError:
    return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)


Comment.objects.all()

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
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# New Feed View
class UserFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

class CommentListCreateView(generics.ListCreateAPIView):
    # ... (existing code for comments)
    pass

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # ... (existing code for comments)
    pass


# New LikePostView
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Try to create a like
            Like.objects.create(user=request.user, post=post)
            # Create a notification for the post author
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked',
                    target=post
                )
            return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"message": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
