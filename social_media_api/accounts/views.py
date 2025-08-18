from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, UserSerializer
from .models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser
from notifications.models import Notification # Import Notification model
from django.contrib.contenttypes.models import ContentType # Import ContentType


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        request.user.following.add(user_to_follow)
        return Response({"message": "User followed"}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response({"message": "User unfollowed"}, status=status.HTTP_200_OK)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )

class UserLoginView(TokenObtainPairView):
    pass

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'




class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
            if request.user.id == user_id:
                return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

            if user_to_follow in request.user.following.all():
                return Response({"error": f"You are already following {user_to_follow.username}."}, status=status.HTTP_400_BAD_REQUEST)

            request.user.following.add(user_to_follow)
            # Create a notification for the user being followed
            Notification.objects.create(
                recipient=user_to_follow,
                actor=request.user,
                verb='followed',
                target=request.user # The actor (follower) is the target in this context
            )
            return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            if user_to_unfollow not in request.user.following.all():
                return Response({"error": f"You are not following {user_to_unfollow.username}."}, status=status.HTTP_400_BAD_REQUEST)

            request.user.following.remove(user_to_unfollow)
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)