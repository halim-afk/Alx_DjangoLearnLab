from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.ReadOnlyField(source='recipient.username')
    actor = serializers.ReadOnlyField(source='actor.username')
    # Custom field to represent the target object
    target_object_representation = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'timestamp', 'read', 'target', 'target_object_representation']

    def get_target_object_representation(self, obj):
        if obj.target:
            return str(obj.target)
        return None