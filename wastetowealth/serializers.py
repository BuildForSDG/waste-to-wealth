from django.contrib.auth.models import Group
# from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from rest_auth.registration.serializers import RegisterSerializer

# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

class UserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(
    #     required = True,
    #     validators = [UniqueValidator(queryset=get_user_model().objects.all())]
    #     )

    username = serializers.CharField(
        max_length=32,
        validators = [UniqueValidator(queryset=CustomUser.objects.all())]
    )
    
    # password1 = serializers.CharField(min_length=8, write_only=True)
    # password2 = serializers.CharField(min_length=8, write_only=True)

    # group = GroupSerializer(source='groups', many=True)

    # def validate(self, data):
    #     if data['password1'] != data['password2']:
    #         raise serializers.ValidationError('Passwords must match')
    #     return data

    # def create(self, validated_data):
    #     ''' Creates and return a new user.'''

    #     data = {
    #         key:value for key, value in validated_data.items()
    #         if key not in ('password1', 'password2')
    #     }
    #     data['username'] = validated_data['username']
    #     data['password'] = validated_data['password1']
    #     data['email'] = validated_data['email']
    #     user = self.Meta.model.objects.create_user(**data)
    #     user.save()
    #     return user
    
    # def update(self, instance, validated_data):
    #     '''Updates an authenticated user.'''

    #     password = validated_data.pop('password', None)
    #     user = super().update(instance, validated_data)

    #     if password:
    #         user.set_password(password)
    #         user.save()

    #     return user
    address = serializers.CharField(
        required=False,
        max_length=100,
    )
    cac_id = serializers.CharField(
        required=False, 
        max_length=100,
    )

    first_name = serializers.CharField(
        required=True,
        max_length=100,
    )
    last_name = serializers.CharField(
        required=True,
        max_length=100,
    )

    def get_first_name(self, obj):
        return obj.first_name.title()

    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'first_name', 'last_name', 'address', 'cac_id']
        read_only_fields = ['id']

class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(
        max_length=32,
        validators = [UniqueValidator(queryset=CustomUser.objects.all())]
    )
    first_name = serializers.CharField(
        required=True,
        max_length=100,
    )
    last_name = serializers.CharField(
        required=True,
        max_length=100,
    )

    address = serializers.CharField(
        required=False,
        max_length=100,
    )
    cac_id = serializers.CharField(
        required=False, 
        max_length=100,
    )

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        data_dict['address'] = self.validated_data.get('address', '')
        data_dict['cac_id'] = self.validated_data.get('cac_id', '')
        return data_dict

