from rest_framework import serializers
from django.contrib.auth import get_user_model 

UserModel = get_user_model()


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