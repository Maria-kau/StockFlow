from rest_framework import serializers
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)

class UserProfileSerializer (serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "groups"
        )
    def get_groups(self,obj):
        return obj.groups.values_list("name", flat=True)
