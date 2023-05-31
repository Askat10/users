from rest_framework import serializers
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from .utils import send_activation_code, create_activation_code




User = get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=200, write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

        extra_kwargs = {
            'password': {'write_only': True},
        }


# .is_valid()
    def validate(self, attrs: dict):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError({'message': 'Passwords do not match'}, code = status.HTTP_400_BAD_REQUEST)
        return attrs


#  attrs -> validated_data
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        create_activation_code(user)
        send_activation_code(user)
        return user
    

class ActivationSerializer(serializers.Serializer):
    activation_code = serializers.CharField(max_length=10)

    def validate_activation_code(self, activtion_code):
        code_exists = User.objects.filter(activation_code=activtion_code).exists()
        if code_exists:
            return activtion_code
        raise serializers.ValidationError({'message': 'activation code does not match'}, code=status.HTTP_400_BAD_REQUEST)
    
    def activate(self):
        code = self.validated_data.get('activation_code')
        user = User.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128)

    def validate_username(self, username):
        user = User.objects.filter(username=username).exists()
        if not user:
            raise serializers.ValidationError({'message': f'User with name {username} does not exist'}, code=status.HTTP_400_BAD_REQUEST)
        
        return username

    def validate(self, attrs):
        request = self.context.get('request')
        username = attrs.get('username')
        password = attrs.get('password')
        if not(username and password):
            raise serializers.ValidationError({'message': 'Username and password are required'}, code=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password, request=request)
        if user is None:
            raise serializers.ValidationError({'message': 'Username or password is wrong'})
        
        attrs['user'] = user
        return attrs
    

# TODO: изменение пароля 
# TODO: восстановление пароля


        