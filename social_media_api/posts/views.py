from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, Like # Ensure Like model is imported
from .serializers import PostSerializer, CommentSerializer, LikeSerializer # Ensure LikeSerializer is imported
from notifications.models import Notification # Import Notification model
from django.contrib.contenttypes.models import ContentType # Import ContentType
from django.db import IntegrityError # Import IntegrityError

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
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
        """
        Sets the author of the post to the current authenticated user.
        """
        serializer.save(author=self.request.user)

class UserFeedView(generics.ListAPIView):
    """
    API endpoint that returns a feed of posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Returns posts from users that the current authenticated user is following.
        """
        # Get all users that the current user is following
        following_users = self.request.user.following.all()
        # Filter posts where the author is in the list of following users
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

class CommentListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing comments for a specific post and creating new comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Returns comments for a specific post identified by post_id from the URL.
        """
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Creates a new comment and associates it with the current user and specified post.
        Also creates a notification for the post's author if different from the commenter.
        """
        # Retrieve the post object using the post_id from URL kwargs
        post = Post.objects.get(id=self.kwargs['post_id'])
        # Save the comment, linking it to the current user and the post
        comment = serializer.save(author=self.request.user, post=post)
        
        # Create a notification for the post author if they are not the commenter
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb='commented on',
                target=post # The post object itself is the target
            )

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a specific comment.
    """
    queryset = Comment.objects.all() # Used to retrieve individual comment objects
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_url_kwarg = 'comment_id' # Specifies the URL keyword argument to use for lookup

# New LikePostView
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
        try:
            # Attempt to retrieve the post by its primary key
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Try to create a new Like object. If a like already exists from this user for this post,
            # an IntegrityError will be raised due to unique_together constraint in the Like model.
            Like.objects.create(user=request.user, post=post)
            
            # Create a notification for the post author if they are not the liker
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked',
                    target=post # The post object itself is the target
                )
            return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # Handle the case where the user has already liked the post
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles unliking a post.
        """
        try:
            # Attempt to retrieve the post by its primary key
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Find and delete the like object for the current user and post
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"message": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            # Handle the case where the user has not liked this post
            return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
