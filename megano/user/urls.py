from django.urls import path, include
from user.views import *

app_name = 'user'

urlpatterns = [
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-up', SignUpView.as_view(), name='sign-up'),
    path('sign-out', signOut),
    path("profile", ProfileView.as_view(), name="profile"),
    path('profile/password', ChangePasswordView.as_view(), name='password'),
    path('profile/avatar', ChangeAvatarView.as_view(), name='avatar'),
]