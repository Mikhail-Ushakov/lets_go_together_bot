from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .models import User, Interests


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


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        all_interests = Interests.objects.all()
        user_interests_list = []
        for i in request.data.getlist('interests'):
            interes = all_interests.get_or_create(name=i)
            user_interests_list.append(interes[0].id)
        instance.interests.clear()
        serializer = self.get_serializer(instance, data={'interests': user_interests_list}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)