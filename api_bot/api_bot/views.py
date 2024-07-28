from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
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
    

class SearchUser(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        from_user = get_object_or_404(User, user_id=user_id)
        not_liked_users = from_user.not_liked.values_list('user_id', flat=True)
        liked_users = from_user.liked.values_list('user_id', flat=True)
        skip_users = from_user.delay_users.values_list('user_id', flat=True)
        user_interests = from_user.interests.values_list('id', flat=True)
        searched_users = User.objects.filter(interests__in=user_interests).exclude(Q(user_id=user_id) | Q(user_id__in=not_liked_users) | Q(user_id__in=liked_users) | Q(user_id__in=skip_users)).distinct()
        if not searched_users.exists():
            searched_users = User.objects.all().exclude(Q(user_id=user_id) | Q(user_id__in=liked_users) | Q(user_id__in=skip_users) | Q(user_id__in=not_liked_users)).distinct()
            if not searched_users.exists():
                from_user.not_liked.clear()
                searched_users = User.objects.filter(interests__in=user_interests).exclude(Q(user_id=user_id) | Q(user_id__in=liked_users)).distinct()
        searched_users = searched_users.annotate(same_interests=Count('interests')).order_by('-same_interests')[:5]
        serializer = self.get_serializer(searched_users, many=True)
        return Response(serializer.data)
    

class DelayUserView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.DelayUserSerializer
    lookup_field = 'user_id'


class NotLikedView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.NotLikedUserSerializer
    lookup_field = 'user_id'
    

class LikedView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.LikedUserSerializer
    lookup_field = 'user_id'
    
    def patch(self, request, *args, **kwargs):
        self_user = self.get_object()
        serializer = self.get_serializer(self_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            other_user_id = serializer.data.get('liked')[0]
            other_user = get_object_or_404(User, user_id=other_user_id) 
            if self_user in other_user.liked.all():
                self_user.matches.add(other_user)
                self_user.save()
                return Response(status=201, data={'other_username': other_user.username})
            else:
                return Response(status=201, data={'other_username': None})

        return Response(status=400, data="wrong parameters")
    

class MyMatchesView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'user_id'

    def get(self, request, *args, **kwargs):
        self_user = self.get_object()
        matches = self_user.matches.all().values_list('username', flat=True)
        return Response(matches)
    

class MyDelayView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'user_id'

    def get(self, request, *args, **kwargs):
        self_user = self.get_object()
        delay_forms = self_user.delay_users.all()
        serializer = self.get_serializer(delay_forms, many=True)
        return Response(serializer.data)