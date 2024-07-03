from rest_framework import serializers
from django.contrib.auth import get_user_model 

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            user_id=validated_data['user_id'],
            is_staff=False            
        )

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        # fields = ( "user_id", "name", "gender", "age", "city", "interests", "date", "description", "user_avatar")
        fields = '__all__'