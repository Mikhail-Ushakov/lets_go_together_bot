from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .models import User


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ProfileView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer
    lookup_field = 'user_id'


class UserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'user_id'


class SetPhotoView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.SetPhotoSerializer
    lookup_field = 'user_id'


class SetDescriptionView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.SetDescriptionSerializer
    lookup_field = 'user_id'


class SetDateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.SetDateSerializer
    lookup_field = 'user_id'


class SetInterestsView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.SetInterestsSerializer
    lookup_field = 'user_id'

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        # user.interests.add(*serializer.data)
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return super().patch(request, *args, **kwargs)
        # serializer.save()