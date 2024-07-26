from rest_framework import serializers
from django.contrib.auth import get_user_model 
from .models import Interests
UserModel = get_user_model()


class InterestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interests
        fields = ['name']

class UserRegisterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            user_id=validated_data['user_id'],
            name=validated_data['name'],
            is_staff=False            
        )

        return user

    class Meta:
        model = UserModel
        fields = ("user_id", "name")


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ("name", "age", "gender", "city")


class UserSerializer(serializers.ModelSerializer):
    interests = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = UserModel
        fields = '__all__'


class SetPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('user_avatar',)


class SetDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('description',)


class SetDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('date',)


class SetInterestsSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = UserModel
        fields = ('interests',)


class DelayUserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = UserModel
        fields = ('delay_users',)

    def update(self, instance, validated_data):
        instance.delay_users.add(validated_data.get('delay_users')[0])
        instance.save()
        return instance
    

class NotLikedUserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = UserModel
        fields = ('not_liked',)

    def update(self, instance, validated_data):
        other_user = validated_data.get('not_liked')[0]
        instance.not_liked.add(other_user)
        if instance.delay_users.filter(user_id=other_user.user_id).exists():
            instance.delay_users.remove(other_user)
        instance.save()
        return instance


class LikedUserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = UserModel
        fields = ('liked',)

    def update(self, instance, validated_data):
        other_user = validated_data.get('liked')[0]
        instance.liked.add(other_user)
        if instance.delay_users.filter(user_id=other_user.user_id).exists():
            instance.delay_users.remove(other_user)
        instance.save()
        return instance
