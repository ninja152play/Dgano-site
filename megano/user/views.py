import json
import os
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from user.models import *
from user.serializers import *

User = get_user_model()

# Create your views here.
class SignInView(APIView):
    def post(self, request):
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get('username')
        password = user_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request):
        user_data = json.loads(next(iter(request.data.keys())))
        name = user_data.get('name')
        if name == '':
            name = 'name'
        username = user_data.get('username')
        password = user_data.get('password')

        try:
            if User.objects.filter(username=username).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username,
                                            password=password)
            avatar, _ = AvatarImage.objects.get_or_create(src='app_user/avatars/default.png',
                                                alt='Default avatar')
            profile = Profile.objects.create(user=user, fullName=name, avatar=avatar)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        avatar = request.data.pop('avatar')
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        old_password = request.data['currentPassword']
        new_password = request.data['newPassword']
        if not profile.user.check_password(old_password):
            return Response({'message': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        profile.user.set_password(new_password)
        profile.user.save()
        return Response({'message': 'Password changed'}, status=status.HTTP_200_OK)


class ChangeAvatarView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        avatar_file = request.FILES.get('avatar')
        if avatar_file:
            avatar = AvatarImage.objects.create(src=avatar_file, alt=str(avatar_file))
            profile.avatar = avatar
            profile.save()
            return Response({'message': 'Avatar changed'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid file'}, status=status.HTTP_400_BAD_REQUEST)
