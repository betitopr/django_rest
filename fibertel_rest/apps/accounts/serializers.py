from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import ClientProfile

User = get_user_model()

class ISPTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para JWT que incluye información adicional
    relevante para el sistema ISP en el token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Añadir claims específicos del ISP
        token['email'] = user.email
        token['is_client'] = user.is_client
        if user.is_client:
            token['service_status'] = user.client_profile.service_status
        
        return token

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo de Usuario con campos seguros para la API.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 
                 'last_name', 'phone_number', 'is_client')
        read_only_fields = ('id',)

class ClientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    
    class Meta:
        model = ClientProfile
        fields = ('id', 'user', 'user_id', 'document_type', 
                 'document_number', 'service_status', 'installation_coordinates')

    def create(self, validated_data):
        return ClientProfile.objects.create(**validated_data)
    
    