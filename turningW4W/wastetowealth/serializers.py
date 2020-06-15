from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=get_user_model().objects.all())]
        )
    username = serializers.CharField(
        max_length=32,
        validators = [UniqueValidator(queryset=get_user_model().objects.all())]
    )
    password1 = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    group = GroupSerializer(source='groups', many=True)

    def create(self, validated_data):
        ''' Creates and return a new user.'''

        group_data = validated_data.pop('group')
        group, _ = Group.objects.get_or_create(name=group_data)
        data = {
            key:value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['username'] = validated_data['username']
        data['password'] = validated_data['password1']
        data['email'] = validated_data['email']
        user = self.Meta.model.objects.create_user(**data)
        user.groups.add(group)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        '''Updates an authenticated user.'''

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ['id','first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'group']
        read_only_fields = ['id']

