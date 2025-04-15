from rest_framework import serializers
from user.models import *


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()
    class Meta:
        model = AvatarImage
        fields = ['src', 'alt']

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = Profile
        fields = ['fullName', 'email', 'phone', 'balance', 'avatar']