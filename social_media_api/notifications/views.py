from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from posts.views import StandardResultsSetPagination # Re-use pagination class from posts app
from accounts.models import User # Import User model
from rest_framework.views import APIView # Import APIView for following notifications

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Fetch notifications for the current authenticated user, ordered by timestamp
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class NotificationMarkAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
            notification.read = True
            notification.save()
            return Response({"message": "Notification marked as read."}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)
# Create your views here.
