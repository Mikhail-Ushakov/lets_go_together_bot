from rest_framework import serializers
from django.contrib.auth import get_user_model 
from .models import Interests
UserModel = get_user_model()


class InterestsSerializer(serializers.ModelSerializer):
    # all_users = serializers.StringRelatedField(many=True)

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
    # interests = serializers.StringRelatedField(many=True, read_only=True)
    interests = InterestsSerializer(many=True)
    def update(self, instance, validated_data):
        # interests = validated_data.pop('interests')
        print(validated_data)
        # instance.title = validated_data.get('title', instance.title)
        # instance.save()
        # for interes in interests:
        #     instance.interests.add(interes)
        # return instance
     
    class Meta:
        model = UserModel
        fields = ('interests',)